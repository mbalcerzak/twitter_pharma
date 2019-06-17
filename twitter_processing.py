import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import collections
import re
#import os

from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
from scipy import stats
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

path = 'C:/Users/malgo_000/Desktop/Web_scraping/twitter_scraping/tweet_texts_pharma/'
#path = os.path.join(os.getcwd(), 'tweet_texts_pharma/')

def prepare_dataset(comp):
    df = pd.read_csv(path + '%s_tweets.txt' % comp, sep='|')

    print(comp + ' : ' + str(len(df)))

    df['company'] = comp
    df['id'] = df['id'].apply(str)
    # cleaning tweet text
    df['hashtags'] = df['text'].apply(lambda s: re.findall(r'#(\w+)', s))
    df['num_hash'] = df['hashtags'].apply(len)
    df['retweet'] = df['text'].apply(lambda s: True if 'RT ' in s else False)
    df['tagged'] = df['text'].apply(lambda s: re.findall(r'@(\w+)', s))

    def clean_tweet(tweet):
        check = '(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)'
        return ' '.join(re.sub(check, ' ', tweet).split()).replace('RT ','')

    df['clean_tweet'] = [clean_tweet(tweet) for tweet in df['text']]
    df['len'] = df['clean_tweet'].apply(len)

    # getting time and date
    df['datetime'] = pd.to_datetime(df['created_at'])
    df['hour'] = df['datetime'].apply(lambda x: x.hour)
    df['month'] = df['datetime'].apply(lambda x: x.month)
    df['day'] = df['datetime'].apply(lambda x: x.day)
    df['year'] = df['datetime'].apply(lambda x: x.year)

    df['z'] = np.abs(stats.zscore(df['fav']))
    df = df[df['z'] < 3]

    return df

def combine_tweets(company_names):
    df_all = df
    for company in company_names:
        df_all = df_all.append(prepare_dataset(company))

    return df_all

company_list = ['JNJCares', 'Roche', 'Pfizer', 'Novartis', 'BayerPharma',
                'Merck','GSK','Sanofi', 'abbvie', 'AbbottGlobal','LillyPad',
                'Amgen','bmsnews','GileadSciences']

df = prepare_dataset('AstraZeneca')
df_all = combine_tweets(company_list)


# average length of all tweets for AZ
print(round(np.mean(df['len'])))
print(round(np.mean(df_all['len'])))

# number of likes for the most liked tweet and average likes
print(np.max(df['fav']))
print(round(np.mean(df['fav'])))

print(np.max(df['fav']))
print(round(np.mean(df['fav'])))

# number of retweets for the most retweeted tweet
print(np.max(df['RT']))

#getting rid of outliers
sns.boxplot(x=df['fav'])
#df['z'] = np.abs(stats.zscore(df['fav']))
#df = df[df['z'] < 3]

# Time series
time_fav = pd.Series(data=df['fav'].values, index=df['created_at'])
time_fav.plot(color = 'r', label = 'favourites', legend = True)

# for retweets
time_rt = pd.Series(data=df['RT'].values, index=df['created_at'])
time_rt.plot(color = 'b', label = 'retweets', legend = True)

# number of hashtags
time_hsh = pd.Series(data=df['num_hash'].values, index=df['created_at'])
time_hsh.plot(color = 'g', label = 'hashtags', legend = True)

plt.figsize=(16, 4)
plt.show()

# barplot of number of hashtags per tweet

df['num_hash'].hist(color = 'b', label = 'numer of hashtags')
plt.show()

counter_hsh = collections.Counter(df['num_hash'])
print(counter_hsh.most_common())


def most_common_words(text):
    lemmatizer = WordNetLemmatizer()

    all_tweets = []
    all_tweets_lem = []

    for tweet in text:
        for word in tweet.split(' '):
            if word.lower() not in stop_words:
                all_tweets.append(word.lower())
                all_tweets_lem.append(lemmatizer.lemmatize(word.lower()))

    return all_tweets, all_tweets_lem

all_tweets, all_tweets_lem = most_common_words(df['clean_tweet'])

# most common words
counter = collections.Counter(all_tweets)
print(counter.most_common(15))

# most common lemmatized words
counter_l = collections.Counter(all_tweets_lem)
print(counter_l.most_common(15))

# most liked tweets od AZ
df.nlargest(3, 'fav')
#df_all.nlargest(15, 'fav')

d = pd.DataFrame(counter.most_common(15), columns = ['Word', 'Count'])
d.plot.bar(x='Word',y='Count')

# worcloud
plt.figure(figsize = (30,30))
wordcloud_ = WordCloud(background_color = 'white',
                       max_words = 1000,
                       max_font_size = 120,
                       width=600, height=400,
                       random_state = 42
                     ).generate(' '.join([a for a in all_tweets]))

#Plotting the word cloud
plt.imshow(wordcloud_)
plt.axis('off')
plt.show()

# most common hashtags
hsh_list= []
for h in list(df['hashtags']):
    hsh_list += h

counter_h = collections.Counter(hsh_list)
print(counter_h.most_common(15))

# wordcloud of hashtags
plt.figure(figsize = (30,30))
wordcloud_ = WordCloud(background_color = 'white',
                       max_words = 1000,
                       max_font_size = 120,
                       width=800 ,height=400,
                       random_state = 42,
                       collocations=False,
                     ).generate(' '.join([a for a in hsh_list]))

plt.imshow(wordcloud_)
plt.axis('off')
plt.show()

# most popular tagged accounts
tag_list= []
for t in list(df['tagged']):
    tag_list += t

counter_t = collections.Counter(tag_list)
print(counter_t.most_common(15))


# number of retweets

ax1 = sns.countplot(df['retweet'], palette='rainbow')
#ax1.set_title('%s's tweets' % company)
ax1.set(xticklabels=['Tweets','Retweets'])

#Number of tweets hourly
hourly_tweets = df_all.groupby(['hour', 'company']).size().unstack()
hourly_tweets.plot(title='Hourly Tweet Counts', colormap='coolwarm')

#Number of tweets by the months
monthly_tweets = df_all.groupby(['month', 'company']).size().unstack()
monthly_tweets.plot(title='Monthly Tweet Counts', colormap='winter')


# stacked
hoursly_tweets_stacked = df_all.groupby(['hour', 'company']).size().unstack()
hoursly_tweets_stacked.plot(kind='bar', stacked=True, colormap='tab20b')



############ ALL PHARMA TWEET DATASETS IN ONE ###########

# overall statistics
mean_fav = df_all.groupby('company')['fav'].mean().astype(int)
mean_fav.sort_values(ascending=False)

mean_rt = df_all.groupby('company')['RT'].mean().astype(int)
mean_rt.sort_values(ascending=False)

mean_len = df_all.groupby('company')['len'].mean().astype(int)
mean_len.sort_values(ascending=False)
