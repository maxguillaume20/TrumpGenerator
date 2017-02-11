# parse_tweets.py
import re

longTweet = ''

def stitch_long_tweets(line):
	if line:
		global longTweet
		conTweet = re.match(r'\.{2,}', line) # if line starts with one or more '.'
		if conTweet:
			conTweet = line[conTweet.end():]
			midTweet = re.search(r'\.{2,}', conTweet)
			if midTweet:
				conTweet = conTweet[:midTweet.start()]
			longTweet = '%s %s' % (conTweet, longTweet)
		elif longTweet:
			try:
				newTweet = '%s %s' % (line[:re.search(r'\.{2,}', line).start()], longTweet)
			except:
				print line
			# print newTweet
			longTweet = ''
			return newTweet
		else:
			return line

def remove_links(line):
	if line:
		newTweet = line
		link = re.search(r'pic\.twitter|http', line)
		if link:
			return None
		return newTweet

def remove_retweets(line):
	if line:
		retweet = re.match(r'" @\w+ :',line)
		if not retweet:
			return line
		else:
			return None


def main():
	inFileName = 'trumptweets.txt'
	outFileName = 'parsed_trumptweets.txt'
	with open(inFileName) as inFile:
		with open(outFileName, 'w') as outFile:
			for line in inFile.readlines():
				newTweet = line.rstrip()
				newTweet = remove_retweets(newTweet)
				newTweet = stitch_long_tweets(newTweet)
				newTweet = remove_links(newTweet)
				if newTweet:
					print>> outFile, newTweet + '\n'
						
					


if __name__ == '__main__':
	main()