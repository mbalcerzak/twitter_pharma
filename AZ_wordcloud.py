import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os

from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

path = os.path.join(os.getcwd(), 'tweet_texts_pharma/')

def prepare_wordlist(comp):
    df = pd.read_csv(path + '%s_tweets.txt' % comp, sep='|')
    all_tweets = []
    
    def clean_tweet(tweet):
        check = '(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)'
        return ' '.join(re.sub(check, ' ', tweet).split()).replace('RT ','')
        
    df['clean_tweet'] = [clean_tweet(tweet) for tweet in df['text']] 
    
    for tweet in df['clean_tweet']:
        for word in tweet.split(' '):
            if word.lower() not in stop_words:
                all_tweets.append(word.lower())
   
    return all_tweets

words_list = prepare_wordlist('AstraZeneca')

# make sure that the wordcloud is shaped as AZ logo
az_mask = np.array(Image.open(path + 'az_symbol.png'))

# make the cloud in AZ official colours
az_colors = ImageColorGenerator(az_mask)

plt.figure(figsize = (10,10))
wordcloudAZ = WordCloud(background_color = 'white',
                        max_words = 1000,
                        max_font_size = 140,
                        width=1200, height=1000,
                        random_state = 42,
                        mask = az_mask,
                        contour_color='gold',
                        contour_width=1,
                      ).generate(' '.join([a for a in words_list]))

plt.imshow(wordcloudAZ.recolor(color_func=az_colors), interpolation='bilinear')
plt.axis('off')
plt.show()