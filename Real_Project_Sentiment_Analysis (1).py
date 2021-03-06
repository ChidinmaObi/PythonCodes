# -*- coding: utf-8 -*-
"""Real Project Sentiment Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-hxZtE1sywnniKp2q2aH8sIkNBUm-IHM
"""

from google.colab import drive
drive.mount('/content/drive')

import re, nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv("/content/drive/My Drive/Nigerian_Inflation_Tweets.csv", encoding = "ISO-8859-1")

pd.set_option('display.max_colwidth', None) # Setting this so we can see the full content of cells

# Cleaning Tweets
def cleaner(text):
  text= re.sub(r'@[A-Za-z0-9]+', '', text)#remove @mentions
  text= re.sub(r'#', '', text) #Removing the # symbol
  text= re.sub(r'RT[\s]+', '', text) #Removing retweet
  text= re.sub(r'https?:\/\/\S+', '', text) #Remove the hyperlinks

  return text

df['cleaned_tweet'] = df.TWEETS.apply(cleaner)
#Show cleaned text
df

#create Function to get subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity
#create Function to get polarity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

df['Subjectivity'] = df.cleaned_tweet.apply(getSubjectivity)
df['Polarity'] = df.cleaned_tweet.apply(getPolarity)

#Show new dataframe with the new column
df

allWords = ' '. join ([twts for twts in df['cleaned_tweet']])
wordCloud = WordCloud(width=500, height=300, random_state= 21, max_font_size = 119).generate(allWords)

plt.imshow(wordCloud,interpolation= "bilinear")
plt.axis('off')
plt.show()

#Create Function to compute the negative ,neutral and positive analysis
def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score== 0:
    return 'Neutral'
  else:
    return 'Positive'
  
df['Analysis']= df['Polarity'].apply(getAnalysis)

#Show the dataframe
df

# Plot the polarity and subjectivity
plt.figure(figsize=(8,6))
for i in range(0, df.shape[0]):
  plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color='Blue' )

plt.title('Sentiment Analysis of Nigerian Inflation data')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()

#Get the Percentage of positive tweets
ptweets=df[df.Analysis == 'Positive']
ptweets= ptweets['cleaned_tweet']

round( (ptweets.shape[0] / df.shape[0]) *100,1)

#Get Percentage of negative tweets
Nvetweets=df[df.Analysis == 'Negative']
Nvetweets= Nvetweets['cleaned_tweet']

round( (Nvetweets.shape[0] / df.shape[0]) *100,1)

#Get Percentage of Neutral tweets
Neutweets=df[df.Analysis == 'Neutral']
Neutweets= Neutweets['cleaned_tweet']

round( (Neutweets.shape[0] / df.shape[0]) *100,1)

#Show the value counts
df['Analysis'].value_counts()

#plot and visualize the counts
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind= 'bar')

df.to_csv('/content/drive/My Drive/Sentiment_Analysis_Data.csv')





