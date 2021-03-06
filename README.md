# Pharmaceutical companies Twitter analysis (using NLP)

The reason behind creating this project is to analyse Pharma tweets using NLP methods in Python 3. I came up with that idea after stumbling upon Harvard Business Review [Twitter empathy scorings from 2015](https://twitter.com/harvardbiz/status/805712993384353792) and their article ["50 Companies That Get Twitter – and 50 That Don’t"](https://hbr.org/2015/04/the-best-and-worst-corporate-tweeters) by Belinda Parmar. I noticed that my company was **the last one** out of 300 and decided to check why is that myself

<img align="right" width="460" height="600" src="https://github.com/mbalcerzak/twitter_pharma/blob/master/az_.png">


## Project structure

1. Found a business problem to work on - ["50 Companies That Get Twitter – and 50 That Don’t"](https://hbr.org/2015/04/the-best-and-worst-corporate-tweeters). Has any of the comapnies discovered how to communicate better on Twitter? What are the industry "standards" on this social media channel?
2. Scraped data from 15 highest-earning pharmaceutical companies' Twitter accounts
3. Cleaned data
4. Explored data and created a document in Jupyter Notebook to show the code, outputs and my comments
5. Visualised the outcomes
6. Presented it in front of the stakeholders at my company

## Project files

**data_analysis** - contains the Jupyter Notebook document and code that created a wordcloud shaped like AZ's logo  
**web_scraping** - contains code used to scrape tweets of selected companies  

## Packages used

```python
import pandas as pd
import numpy as np
import tweepy
import csv
import time
import re
import os
import wordcloud
import matplotlib.pyplot as plt
import nltk
import PIL

import scipy
import collections
import seaborn as sns
```

## Data scources and refereces
- https://en.wikipedia.org/wiki/List_of_largest_pharmaceutical_companies_by_revenue
- 15 most profitable companies Twitter accounts
- https://developer.twitter.com/en/docs
