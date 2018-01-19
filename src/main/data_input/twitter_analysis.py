"""
Get twitter data from database or flat file, and perform the analysis
"""
import json
import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
from textblob import TextBlob
from tweet import Tweet  # from the module, file name might change


t = Tweet(tweet_file='tweet_file.txt')

tweets = t.get_tweets()  # if read from file, it's a list of dict

# t_id, text, time = [], [], []


df = pd.DataFrame.from_records(tweets)
# print(list(df.columns.values))

texts = df['text']

text_blobs = [TextBlob(text) for text in texts]
print(text_blob.sentiment for text_blob in text_blobs)


#
# # print (tweets[0]['text'])
# tweets_text = [tweet['text'] for tweet in tweets]
#
#
# for tweet in tweets:
#     print(tweet['text'])

# ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
# ts = ts.cumsum()
# ts.plot()

# df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index,
#                       columns=['A', 'B', 'C', 'D'])
# df = df.cumsum()
# plt.figure()
# # df.plot()
# plt.legend(loc='best')
# plt.show()
