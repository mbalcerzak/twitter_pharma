import simplejson as json
import tweepy
import csv
import pandas as pd     # To handle data
import numpy as np      # For number computing
import os
import unicodedata

# For plotting and visualization:
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns

#Twitter API credentials
consumer_key = "8bLIFLRBX1mMvicwJYl7Uh57k"
consumer_secret = "cxjaFxSCGv7awlbAVDQnmaItITI9TNxTvnFDdD7qbntsd9lj5q"
access_key = "1098576703939661824-6pf9AYwb6JzsG8WIKfNU0VdaOLZ629"
access_secret = "z16DSEjQXEZwLKK3D0wWo7SbbGiIUGsGqDCqKu6wdaS4S"

outtweets = []


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify = True)

    a = 0

    for tweet_info in tweepy.Cursor(api.user_timeline, id='AstraZeneca', tweet_mode='extended').items():
        if 'retweeted_status' in dir(tweet_info):
            tweet='RT ' + tweet_info.retweeted_status.full_text
            likes = tweet_info.retweeted_status.favorite_count
        else:
            tweet=tweet_info.full_text
            likes = tweet_info.favorite_count
        
        #print(tweet)
        a += 1
        if a%1000==0: print(a)      

        outtweets.append([tweet_info.id_str, tweet_info.created_at, tweet, tweet_info.source, 
                  likes, tweet_info.retweet_count, tweet_info.entities.get('hashtags')])
    

    #write the csv  
    with open('%s_tweets.txt' % screen_name, 'w',  encoding="utf8") as f:
        writer = csv.writer(f, delimiter = '|')
        writer.writerow(["id","created_at","text", "source", "fav", "RT", "hashtags"])
        writer.writerows(outtweets)
    
    # pass


#if __name__ == '__main__':
	#pass in the username of the account you want to download


company_names = ["AstraZeneca", "JNJCares", "Roche", "Pfizer","Novartis","BayerPharma","Merck","GSK","Sanofi","abbvie",
                "AbbottNews","AbbottGlobal","LillyPad","Amgen","bmsnews","GileadSciences"]

for company in company_names:
	get_all_tweets(company)


