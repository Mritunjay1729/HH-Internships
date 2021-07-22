# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 19:00:05 2021

@author: MRITYUNJAY
Sentimental Analysis on ISEGlobal
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('finalData.csv')
data.columns
data.drop('Unnamed: 0', inplace = True, axis = 1)
data.groupby('Platform').describe()
data
data.drop_duplicates(keep = 'first', inplace = True, ignore_index = True)

#Converting to lower text
clean_text = [i.lower() for i in data['Content (Reviews and Tweets)']]


#Tokenize
#sentence tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
sent_tok = []
for sent in clean_text:
    sent = sent_tokenize(sent)
    sent_tok.append(sent)
sent_tok

#word tokenize
clean_text_2 = [word_tokenize(i) for i in clean_text]
clean_text_2

#remove punctuations
import re
clean_text_3 = []
for words in clean_text_2:
    clean = []
    for word in words:
        res = re.sub(r'[^\w\s]', "",  word)
        if(res != ""):
            clean.append(res)
    clean_text_3.append(clean)
clean_text_3

#remove Stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords

clean_text_4 = []
for words in clean_text_3:
    clean = []
    for word in words:
        if not word in stopwords.words('english'):
            clean.append(word)
    clean_text_4.append(clean)
clean_text_4

#Stemming - removing the ings, ed, s etc to bring word back to its root form
from  nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('wordnet')
lemma = WordNetLemmatizer()
stemm = SnowballStemmer('english')

#Just showing uses for my own sake
a = [stemm.stem(i) for i in ['reading', 'washing', 'driving', 'drive']]
b = [lemma.lemmatize(i, 'v') for i in ['reading', 'washing', 'driving', 'cooking']]       
b

clean_text_5 = []
for words in clean_text_4:
    clean = []
    for word in words:
        w_stemmed = stemm.stem(word)
        clean.append(w_stemmed)
    clean_text_5.append(clean)
    
clean_text_5

#Lemmatization
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('wordnet')
lemma = WordNetLemmatizer()

lem = []
for words in clean_text_4:
    clean = []
    for word in words:
        w_lemma = lemma.lemmatize(word)
        clean.append(w_lemma)
    lem.append(clean)
lem

#Vectorization
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(ngram_range=(1,2))
X_vec = [cv.fit_transform(i).toarray() for i in lem]
X_vec
print(cv.get_feature_names())

#Get Test Value.. Similarily perform Vectorization on that value.

#Sentiment Ananlysis

#!pip install vaderSentiment textblob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
lem

#Using TextBlob
analysis = [TextBlob(i) for i in data['Content (Reviews and Tweets)']]
analysis
analysis[0].tags
sentiment_1 = [i.sentiment for i in analysis]
data['Content (Reviews and Tweets)'][0]
polarity = [i.polarity for i in sentiment_1]
subjectivity = [i.subjectivity for i in sentiment_1]
polarity, subjectivity
sentiment_data = data 
len(polarity)
len(subjectivity)
data['polarity'] = polarity
data['subjectivity'] = subjectivity 
pd.set_option('max_rows', 25)
data[['Content (Reviews and Tweets)', 'polarity']].groupby('polarity').head(25)
data[data['polarity'] < 0]['Content (Reviews and Tweets)'].tail(25)
data.to_csv('TextBlobSentiment.csv')

sm = SentimentIntensityAnalyzer()
sentiment = [TextBlob.sentiment(i) for i in lem]

#Using VaderSentiment
vader = SentimentIntensityAnalyzer()
analysis = [vader.polarity_scores(i) for i in data['Content (Reviews and Tweets)']]
df_analysis = pd.DataFrame(analysis)
dt_new = pd.concat([data, df_analysis], axis=1)
dt_new.to_csv('ISELVaderAnalysis.csv')


threshhold = 0.5

def emotion_detect(field):
    sentiment = []
    for i in field:
        if i >= threshhold :
            sentiment.append("Positive")
        elif i <= - threshhold :
            sentiment.append("Negative")
        else :
            sentiment.append("Neutral")
    return sentiment
            
dt_new['Sentiment'] = emotion_detect(dt_new['compound'])
dt_new.to_csv('ISELVaderAnalysis.csv')

def top_n_reviews(df, data_column, number_of_rows, type_of_review):
    print(f"Top {type_of_review} Comments:")
    for index, row in df.nlargest(number_of_rows, data_column).iterrows():
        print(f"Score: {row[data_column]}, Review: {row[1]}")
        

top_n_reviews(dt_new, 'pos', 15, "Positive")
top_n_reviews(dt_new, 'neg', 15, "Negative" ) 

#what are the courses available
ise = pd.read_csv('iselglobal_website.csv')
ise.columns
courses = ise['rv-course 2'].unique()
courses = courses[~pd.isnull(courses)]
courses = list(courses)
courses = [i.lower() for i in courses]
courses
courses = [i.replace("certification", "") for i in courses]
lem = pd.Series(lem)
ab = pd.concat([lem, data['Content (Reviews and Tweets)']], axis = 1)
ab.to_csv('cleaned_words.csv')

