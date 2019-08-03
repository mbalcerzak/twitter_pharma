# Pharmaceutical companies NLP Twitter analysis

The reason behind creating this project is to analyse Pharma tweets using NLP methods in Python 3. I came up with that idea after stumbling upon Harvard Business Review [Twitter empathy scorings from 2015](https://twitter.com/harvardbiz/status/805712993384353792) and their article ["50 Companies That Get Twitter – and 50 That Don’t"](https://hbr.org/2015/04/the-best-and-worst-corporate-tweeters) by
Belinda Parmar

## Project structure

1. Found a business problem to work on - ["50 Companies That Get Twitter – and 50 That Don’t"](https://hbr.org/2015/04/the-best-and-worst-corporate-tweeters). Is any pharmaceutical company doing something differenlty than others? What are the industry "standards" on Twitter?
2. Scraped data from 15 highest-earning pharmaceutical companies' Twitter accounts
3. Cleaned data
4. Explored data and created a document in Jupyter Notebook to show the code, outputs and my comments
5. Visualised the outcomes
6. Presented it in front of the stakeholders at my company

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

from scipy import stats
import collections
from collections import Counter
import seaborn as sns
```

## Data scources and refereces
- https://en.wikipedia.org/wiki/List_of_largest_pharmaceutical_companies_by_revenue
- 15 largest companies Twitter accounts
- https://developer.twitter.com/en/docs
