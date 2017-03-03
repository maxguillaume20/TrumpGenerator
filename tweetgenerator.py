class Base(object):

	def __init__(self):
		self.api = None             # Twitter API
		self.in_tweets = []         # Tweets used for training model 
		self.out_tweets = []        # Generated tweets

	def connectToTwitterAPI(self, consumer_key, consumer_secret, access_token, access_token_secret):

		"""
		Connects to Twitter API using tweepy module. 
		Requires a Twitter account and creating a Twitter App with key and tokens.
		"""
		import tweepy

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)
		self.api = api
		return False

	def retrieveTweets(self, username = None, query_search = None, since = None, until = None, max_tweets = 1, overwrite = False, export_filename = None):
		
		"""
		Retrieves tweets using GetOldTweets module from @Jefferson-Henrique
		https://github.com/Jefferson-Henrique/GetOldTweets-python.
		Can update in_tweets, parse tweets and export to file.
		"""

		import got

		if username == None and query_search == None:
			print "Must specify at least 'username' or at least 'query_search'."
			return None

		criteria = got.manager.TweetCriteria()

		if username:
			criteria.setUsername(username)

		if query_search:
			criteria.setQuerySearch(query_search)

		if since:
			criteria.setSince(since)

		if until:
			criteria.setUntil(until)

		if max_tweets:
			criteria.setMaxTweets(max_tweets)

		self.in_tweets += got.manager.TweetManager.getTweets(criteria)
		return None

	def postTweets(self, tweets = [], require_confirmation = True):

		"""
		Posts a list of tweets.
		"""

		if self.api == None:
			print "Please connect to Twitter using 'connectToTwitterAPI' before running this function."
			return None

		# Handle case where user gives a string
		if type(tweets) is str or type(tweets) is unicode:
			tweets = [tweets]

		# Handle case where user does not give any argument
		# Posts all outputted tweets
		if tweets == []:
			tweets = self.out_tweets

		if not all([type(x) is str or type(x) is unicode for x in tweets]):
			print "Invalid 'tweets' argument: must be a list of strings."
			return False

		# Faire en sorte qu'aucun tweet ne depasse plus de 140 characteres.

		if require_confirmation:
			print "You are about to tweet the following:"
			for x in tweets:
				print "\t" + x + "\n"

			ans = raw_input("Continue (Yes/n?):")
			if ans != "Yes":
				print "Aborted..."
				return False

		print "Currently tweeting..."
		for x in tweets:
			status = self.api.update_status(status = x)
		return None

	def importInTweets(self, filename, overwrite = False):

		"""
		Import input tweets by reading pickle python object file
		"""

		import pickle

		f = open(filename, 'rb')
		if overwrite:
 			self.in_tweets += pickle.load(f)
 		else:
 			self.in_tweets = pickle.load(f)
 		f.close()

		return None

	def exportInTweets(self, filename):

		"""
		Export input tweets to pickle python object file
		"""

		import pickle

		f = open(filename, 'wb')
 		pickle.dump(self.in_tweets, f, pickle.HIGHEST_PROTOCOL)
 		f.close()

		return None

	def writeOutTweets(self, filename):

		"""
		Write generated tweets to txt file.
		"""

		f = open(filename, 'wb')
		for x in self.out_tweets:
			print >> f, x
		f.close()

		return None

	def parseTweets(self, remove_links = True, remove_retweets = True, stitch_long_tweets = True):

		"""
		Cleans up tweets by removing retweets, stitching long tweets and removing links.
		"""

		import re

		def _remove_links_(x):
			x = re.sub(r"http\S+", "", x)
			x = re.sub(r'pic\.twitter\.com\/\S+', '', x)
			x = re.sub(r'bit\.ly\/\S+', '', x)
			x = x.strip()
			return x

		def _is_not_retweet_(x):
			return not re.match(r'" @\w+ :',x)

		parsed_tweets = self.in_tweets

		if stitch_long_tweets:
			pass

		if remove_retweets:
			parsed_tweets = [x for x in parsed_tweets if _is_not_retweet_(x)]

		if remove_links: 
			parsed_tweets = [_remove_links_(x) for x in parsed_tweets]

		self.in_tweets = parsed_tweets

class MarkovChain(Base):

	def __init__(self):
		self.api = None             # Twitter API
		self.in_tweets = []         # Tweets used for training model 
		self.out_tweets = []        # Generated tweets
		self.markov_dict = {}
		self.seed_dict = {}

	def train(self):

		import re

		if len(self.in_tweets) == 0:
			print "Please add input tweets using 'importTweets' or 'retrieveTweets' before running 'train'."

		markov_dict = {}
		seed_dict = {}

		# This regex finds all the words and some punctuation. 
		# Words with punctuation are counted as different than just their word
		# e.g. boat != boat.
		text = [x.text for x in self.in_tweets]
		text_list = re.findall(r'(\w+([\.\',?!]\w*)?)', " ".join(text))
				
		for i in range(0, len(text_list) - 2, 1):
			tuple_state = (text_list[i][0], text_list[i + 1][0]) # States are two consecutive words. 
			markov_dict[tuple_state] = {}

			if str(text_list[i][0]).endswith('.'):
				seed = text_list[i + 1][0] + ' ' + text_list[i + 2][0]
				if seed not in seed_dict.keys():
					seed_dict[seed] = 1
				else:
					seed_dict[seed] += 1
		for i in range(0,len(text_list) - 2, 1):
			tuple_state = (text_list[i][0], text_list[i + 1][0]) 
			next_word = text_list[i + 2][0]

			# Transitions are the frequencies of the next
			# words following the given state ('w0 w1'),
			# so the next state is 'w1 w2' and so on.
			if next_word not in markov_dict[tuple_state].keys():
				markov_dict[tuple_state][next_word] = 1.0
			else:
				markov_dict[tuple_state][next_word] += 1.0

		# Normalize counts
		for state in markov_dict.keys():
			sum_transitions_count = float(sum(markov_dict[state].values()))
			markov_dict[state] = {w:p / sum_transitions_count for w, p in markov_dict[state].items()}

		sum_seed_count = float(sum(seed_dict.values()))
		seed_dict = {s:p / sum_seed_count for s, p in seed_dict.items()}

		self.markov_dict = markov_dict
		self.seed_dict = seed_dict

		return None

	def generate(self, n = 1, overwrite = False):

		import numpy as np
		import re

		def _generate_(markov_dict, seed_dict):
				seed = np.random.choice (seed_dict.keys(), 1, seed_dict.values())[0]
				tweet = seed
				matchObj = re.match (r'(\S+)\s(\S+)', seed)
				current_state = (matchObj.group(1), matchObj.group(2))
				tweet_probability = 1 	# the probability given the seed (first two words)
				while not tweet.endswith('.'):
					next_word = np.random.choice (markov_dict[current_state].keys(), 1, markov_dict[current_state].values())[0]
					tweet += ' ' + next_word
					tweet_probability *= markov_dict[current_state][next_word] 
					current_state = (current_state[1], next_word)
				# tweet += ' ' + str(tweet_probability) + '\n'
				return tweet

		if self.markov_dict == {} or self.seed_dict == {}:
			print "Please run 'train' function before running 'generate'."
		
		tweets = [_generate_(self.markov_dict, self.seed_dict) for i in xrange(0, n)]

		if overwrite:
			self.out_tweets = tweets
		else:
			self.out_tweets += tweets

		return None
