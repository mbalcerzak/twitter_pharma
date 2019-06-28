import tweepy
import csv
import os

path = os.path.join(os.getcwd(), 'tweet_texts_pharma/')

# Twitter API credentials in a separate .txt file that looks like that:
#   consumer_key = XXXXXXXXXXXXXXXXXXXXXXX
#   consumer_secret = XXXXXXXXXXXXXXXXXXXX
#   access_key = XXXXXXXXXXXX-XXXXXXXXXXXX
#   access_secret = XXXXXXXXXXXXXXXXXXXXXX

keys = {}

for line in open(path + 'twitter_keys.txt', 'r').readlines():
    key, var = line.split("=")
    keys[key.strip()] = var.replace('\n','').strip()

# authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_key'], keys['access_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify = True)

def get_all_tweets(screen_name):
    outtweets = []

    for tweet_info in tweepy.Cursor(api.user_timeline, id = screen_name,
                                    tweet_mode='extended').items():
        # adding a way to add retweeted texts
        if 'retweeted_status' in dir(tweet_info):
            tweet= tweet_info.retweeted_status.full_text
            likes = tweet_info.retweeted_status.favorite_count
            retweet = True
        else:
            tweet = tweet_info.full_text
            likes = tweet_info.favorite_count
            retweet = False

        outtweets.append([tweet_info.id_str, tweet_info.created_at, tweet,
                          retweet, tweet_info.source, likes,
                          tweet_info.retweet_count])

    #write the csv
    with open(path + '%s_tweets.txt' % screen_name, 'w', encoding="utf8") as f:
        writer = csv.writer(f, delimiter = '|')
        writer.writerow(["id","created_at","text", "retweet", "source", "fav",
                         "RT"])
        writer.writerows(outtweets)

    print('Done for ' + screen_name + '. Tweets: ' + str(len(outtweets)))
    print(str(companies.index(company) + 1) + '/' + str(len(companies)))

# Pharmaceutical companies twitter usernames
companies = ["AstraZeneca", "JNJCares", "Roche", "Pfizer","Novartis",
             "BayerPharma","Merck","GSK","Sanofi","abbvie", "AbbottNews",
             "AbbottGlobal","LillyPad","Amgen","bmsnews","GileadSciences"]

for company in companies:
	get_all_tweets(company)
