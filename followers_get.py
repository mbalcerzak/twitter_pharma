import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import csv
import time
import os
import pandas as pd

path = 'C:/Users/malgo_000/Desktop/Web_scraping/twitter_scraping/'
path_f = path + 'followers_ids_pharma/'


CONSUMER_KEY = "8bLIFLRBX1mMvicwJYl7Uh57k"
CONSUMER_SECRET = "cxjaFxSCGv7awlbAVDQnmaItITI9TNxTvnFDdD7qbntsd9lj5q"
ACCESS_KEY = "1098576703939661824-6pf9AYwb6JzsG8WIKfNU0VdaOLZ629"
ACCESS_SECRET = "z16DSEjQXEZwLKK3D0wWo7SbbGiIUGsGqDCqKu6wdaS4S"

auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify = True)

# ======================== scraping a list of followers IDs ================================
# def get_followers(screen_name):
# 	ids = []
# 	while True:
# 	    try:
# 	        for page in tweepy.Cursor(api.followers_ids, screen_name = screen_name).pages():
# 	            ids.extend(page)
# 	        print(screen_name, len(ids))    
# 	    except tweepy.TweepError:
# 	        time.sleep(60*15)
# 	        continue
	
# 	    except StopIteration:
# 	        pass
# 	    break
	
# 	with open('%s_followers_id.txt' % screen_name, 'w',  encoding="utf8") as f:
# 	    f.write('|'.join([str(x) for x in ids]))

# company_names = ["AstraZeneca", "JNJCares", "Roche", "Pfizer","Novartis","BayerPharma",
# 				"Merck","GSK","Sanofi","abbvie", "AbbottNews","AbbottGlobal","LillyPad",
# 				"Amgen","bmsnews","GileadSciences"]


# for company in company_names:
# 	exists = os.path.isfile(path_f + '%s_followers_id.txt' % company)
# 	if exists:
# 		print('The followers list of ' + company + ' already exists. Moving on.')
# 		continue
# 	else:
# 		get_followers(company)

# ======================== getting user info from IDs =====================================

company_names = ["AstraZeneca", "JNJCares", "Roche", "Pfizer","Novartis",
				"BayerPharma", "Merck","GSK","Sanofi", "AbbottNews",
				"AbbottGlobal","LillyPad", "Amgen","bmsnews","GileadSciences"]
# company_names = ["abbvie"]

def get_user_info(company):

	with open(path_f + '%s_followers_id.txt' % company, "r") as f:
		followers_id_list = f.readlines()[0].split('|')

	print(company + ' has ' + str(len(followers_id_list)) + ' followers. Getting data in progress...')

	users_list = []
	bios_list = []
	desc_list = []
	follower_count_list = []
	locations = []
	statuses_list = []
	favourites_count_list = []
	created_at_list = []

	for i, follower in zip(range(len(followers_id_list)), followers_id_list):
		if i%1000 == 0 and i >0 :
			print(str(i) + ' users found so far. (' + round(i/len(followers_id_list)) + '%)')

		try:
			user_id = api.get_user(follower)

			#for user_id in list_members_output:
			users_list.append(user_id._json['id'])
			bios_list.append(user_id._json['screen_name'])
			desc_list.append(user_id._json['description'])
			follower_count_list.append(user_id._json['followers_count'])
			locations.append(user_id._json['location'])
			statuses_list.append(user_id._json['statuses_count'])
			favourites_count_list.append(user_id._json['favourites_count'])
			created_at_list.append(user_id._json['created_at'])
		except tweepy.error.TweepError:
			print("user not found: " + follower)
			continue
	        
	zipped_data = zip(users_list, bios_list, desc_list, 
						follower_count_list, locations, statuses_list,
						favourites_count_list, created_at_list)

	# Creates a pandas dataframe containing user attributes
	output_df = pd.DataFrame(list(zipped_data), columns=['user_id', 
	                                                     'screen_name',
	                                                     'bio',
	                                                     'followers',
	                                                     'locations',
	                                                     'statuses_count',
	                                                     'favourites_count',
	                                                     'created_at'])

	print('FInished getting user info fo: ' + company)

	#write the csv  
	with open(path + 'followers_info/' + '%s_followers_info.txt' % company, 'w',  encoding="utf8") as f:
	    writer = csv.writer(f, delimiter = '|')
	    writer.writerow(list(output_df))
	    writer.writerows(output_df.values)



for company in company_names:
	exists = os.path.isfile(path_f + '%s_followers_id.txt' % company)
	if exists:
		print('The followers list of ' + company + ' exists.')
		if os.path.isfile(path + 'followers_info/' + '%s_followers_info.txt' % company):
			print('List with user info already exists. Moving on.')
		else:
			print('Reading the list in.')
			get_user_info(company)
	else:
		print('The followers list of ' + company + ' does not exists.')
		continue