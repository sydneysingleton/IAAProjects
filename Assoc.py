# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 12:12:30 2019

@author: sydne
"""
import pandas as pd
import nltk
import numpy
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import stop_words
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords 
from collections import Counter
from collections import defaultdict
from sentiment_module import sentiment
from matplotlib import figure
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


ps = PorterStemmer()
office = pandas.read_csv("C:/Users/sydne/Downloads/Cleaned_OfficeData.csv")


#  Remove punctuation


office['line_text']=office['line_text'].str.lower()

office['line_text']=office['line_text'].str.replace('[^\w\s]','')


main_chars=["Jim","Pam","Michael","Dwight","Angela", "Kevin", "Toby", "Andy"]

        
        
characters = dict(zip(main_chars, list1))


office = office[office['speaker'].isin(main_chars)]

grouped_lines = office.groupby(['season','episode','speaker'])['line_text']

list1=[]
for seas, ep in grouped_lines:
    list1.append([seas,ep])

df = pandas.DataFrame(list1)

df[0]=df[0].apply(str) 
df[1]=df[1].apply(str) 

df['SEC']=df[0].str.replace('[^\w\s]','')
df['dirty_words']=df[1].str.replace('[^\w\s]','').str.replace('\d+', '')
df[['season', 'episode', 'character']] = df['SEC'].str.split(expand=True)

df=df.filter(["season", "episode", "character", "dirty_words"])

stops=["i", "me", "my", "myself", "we", "our", "ours", "ourselves", 
       "you", "your", "yours", "yourself", "yourselves", "he", "him", 
       "his", "himself", "she", "her", "hers", "herself", "it", "its",
       "itself", "they", "them", "their", "theirs", "themselves", 
       "what", "which", "who", "whom", "this", "that", "these", 
       "those", "am", "is", "are", "was", "were", "be", "been", 
       "being", "have", "has", "had", "having", "do", "does", "did", 
       "doing", "a", "an", "the", "and", "but", "if", "or", "because",
       "as", "until", "while", "of", "at", "by", "for", "with", "about", 
       "against", "between", "into", "through", "during", "before", 
       "after", "above", "below", "to", "from", "up", "down", "in", "out", 
       "on", "off", "over", "under", "again", "further", "then", "once", 
       "here", "there", "when", "where", "why", "how", "all", "any", "both", 
       "each", "few", "more", "most", "other", "some", "such", "no", "nor", 
       "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", 
       "can", "will", "just", "don", "should", "now"]

pat= r'\b(?:{})\b'.format('|'.join(stops))

df['clean_words'] = df['dirty_words'].str.replace(pat, '')
df['clean_words'] = df['clean_words'].str.replace('\n', '')
final['clean_words']=final['clean_words'].apply(lambda x :re.sub(' +', ' ', x))

df=df.filter(["season", "episode", "character", "clean_words"])

senti = {}
for x in df['clean_words']:
    senti.setdefault('arous', [])
    senti.setdefault('val', [])
    words=x.split()
    arous=[]
    val=[]
    for w in words:
        a = sentiment.sentiment(w)['arousal']
        arous.append(a)
        suma=sum(arous)
        v = sentiment.sentiment(w)['valence']
        val.append(v)
        sumv = sum(val)
    senti['arous'].append(suma)
    senti['val'].append(sumv)

senti_df = pandas.DataFrame(senti)    

final = pandas.concat([df, senti_df], axis = 1)

final['character']=pd.Categorical(final['character'])
final['freq']=final['clean_words'].apply(len)
final['clean_words']=final['clean_words'].apply(lambda x :re.sub(' +', ' ', x))


final['SeasEp'] = str("Season ") + final["season"].map(str) + str(" Episode ") + final["episode"]

final['Arousal']=final['arous']/final['freq']
final['Valence']=final['val']/final['freq']


final.to_csv(r'C:\Users\sydne\Documents\Python\final.csv')


all_text = ' '.join(office['line_text'].tolist())
all_text = all_text.lower()
all_text = all_text.replace('[^\w\s]','')
all_text = ''.join([i for i in all_text if not i.isdigit()])

all_list = all_text.split()

clean_list = [word for word in all_list if word not in stops]

all_text = ' '.join(clean_list)

word_count = office['line_text'].value_counts()

word_df = pandas.DataFrame(word_count)
word_df['index1'] = word_df.index

most_common50 =list(word_df['index1'][0:49])





