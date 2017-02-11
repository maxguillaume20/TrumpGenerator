import got

def main():
	
	def printTweet(descr, t):
		print descr
		print "Username: %s" % t.username
		print "Retweets: %d" % t.retweets
		print "Text: %s" % t.text
		print "Mentions: %s" % t.mentions
		print "Hashtags: %s\n" % t.hashtags
	
	tweetCount = 200
	# Example 1 - Get tweets by username
	tweetCriteria = got.manager.TweetCriteria().setUsername('realDonaldTrump').setMaxTweets(tweetCount)
	tweetList = got.manager.TweetManager.getTweets(tweetCriteria)
	count = 0
	with open ('trumptweets2.txt', 'w') as outFile:
		for i in range(tweetCount):
			try:
				print>> outFile, tweetList[i].text.encode('utf-8') + '\n'
				count += 1
			except:
				continue
	print count
	
	# # Example 2 - Get tweets by query search
	# tweetCriteria = got.manager.TweetCriteria().setQuerySearch('europe refugees').setSince("2015-05-01").setUntil("2015-09-30").setMaxTweets(1)
	# tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	
	# printTweet("### Example 2 - Get tweets by query search [europe refugees]", tweet)
	
	# # Example 3 - Get tweets by username and bound dates
	# tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama").setSince("2015-09-10").setUntil("2015-09-12").setMaxTweets(1)
	# tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	
	# printTweet("### Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']", tweet)

if __name__ == '__main__':
	main()
	