import tweepy
import csv
import time
import os
import pandas as pd

path = os.path.join(os.getcwd(), 'twitter_scraping/')
path_ids = path + 'followers_ids_pharma/'
path_user_info = path + 'followers_info/'

# Twitter API credentials in a separate txt file
keys = {}

for line in open(path + 'twitter_keys.txt', 'r').readlines():
    key, var = line.split("=")
    keys[key.strip()] = var.replace('\n','').strip()

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_key'], keys['access_secret'])

api = tweepy.API(auth,wait_on_rate_limit = True,
                 wait_on_rate_limit_notify = True)

# Companies' Twitter usernames
companies = ["AstraZeneca", "JNJCares", "Roche", "Novartis", "Pfizer",
             "BayerPharma", "Merck","GSK","Sanofi","abbvie", "AbbottNews",
             "AbbottGlobal","LillyPad", "Amgen","bmsnews","GileadSciences"]

# ================= scraping a list of followers IDs =========================
def get_followers_ids(screen_name):
 	ids = []
 	while True:
 	    try:
 	        for page in tweepy.Cursor(api.followers_ids,
                                    screen_name = screen_name).pages():
                 ids.extend(page)
                 print(screen_name, len(ids))
 	    except tweepy.TweepError:
 	        time.sleep(60*15)
 	        continue

 	    except StopIteration:
 	        pass
 	    break

 	with open('%s_followers_id.txt' % screen_name, 'w',  encoding="utf8") as f:
 	    f.write('|'.join([str(x) for x in ids]))

# =================== getting user info from IDs =============================
def get_user_info(company):

    with open(path_ids + '%s_followers_id.txt' % company, "r") as f:
        followers_id_list = f.readlines()[0].split('|')

    print(company + ' has ' + str(len(followers_id_list))
         + ' followers. Getting data in progress...')

    users_list = []
    bios_list = []
    desc_list = []
    follower_count_list = []
    locations = []
    statuses_list = []
    favourites_count_list = []
    created_at_list = []

    users_not_found = []

    for i, follower in zip(range(len(followers_id_list)), followers_id_list):
        if (i + 1) % 1000 == 0:
            print('( {} %) users found.'.format(round(i/len(followers_id_list)))
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
            users_not_found.append(user_id)

    zipped_data = zip(users_list, bios_list, desc_list, follower_count_list,
                      locations, statuses_list, favourites_count_list,
                      created_at_list)

	# Creates a pandas dataframe containing user attributes
    output_df = pd.DataFrame(list(zipped_data), columns=['user_id',
	                                                      'screen_name',
	                                                      'bio',
	                                                      'followers',
	                                                      'locations',
	                                                      'statuses_count',
	                                                      'favourites_count',
	                                                      'created_at'])

    print('Finished getting user info for: ' + company)

	# write the followers info
    with open(path_user_info + '%s_followers_info.txt' % company, 'w',
             encoding="utf8") as f:
        writer = csv.writer(f, delimiter = '|')
        writer.writerow(list(output_df))
        writer.writerows(output_df.values)

	# write the not found ids
    with open(path_user_info + '%s_followers_not_found.txt' % company, 'w',
            encoding="utf8") as f:
        f.write('|'.join([str(x) for x in users_not_found]))

# =================== scraping the data =============================
for company in companies:
    exists = os.path.isfile(path_ids + '%s_followers_id.txt' % company)

    if exists:
        print('The followers list of ' + company + ' exists.')

        if os.path.isfile(path_user_info + '%s_followers_info.txt' % company):
            print('List with user info already exists. Moving on.')
        else:
            print('Reading the list in.')
            get_user_info(company)
    else:
        print('The followers list of ' + company + ' does not exists.')
        print('Getting it.')
        get_followers_ids(company)

        print('Reading the list in.')
        get_user_info(company)
