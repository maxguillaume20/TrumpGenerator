#!/usr/bin/python2

"""
Main script to make big boy Drumpf post a tweet or seven.
"""

import tweetgenerator
from key_and_token import kt

drumpf = tweetgenerator.MarkovChain()
drumpf.connectToTwitterAPI(kt['consumer_key'], 
  kt['consumer_secret'], 
  kt['access_token'], 
  kt['access_token_secret'])

drumpf.retrieveTweets(username = "realDonaldTrump", max_tweets = 0)
# drumpf.parseTweets()
# drumpf.importInTweets("trump.pkl", overwrite = False)
drumpf.exportInTweets("trump.pkl")

drumpf.train()
drumpf.generate(n = 1, overwrite = True)

drumpf.postTweets(require_confirmation = True)
