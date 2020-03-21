#!/usr/bin/env python3

#Housekeeping imports
import os
import os.path
from os import path
import sys
import time
from datetime import datetime
import shutil
import random
#Module specific imports
import twitter as tw
import TKEYS as KEYS
#Data science imports
import pandas as pd
import numpy as np
import scipy as scy
import sklearn
import h5py
import tensorflow as tf
import keras
import collections
from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Bidirectional, Embedding
from keras.callbacks import ModelCheckpoint
#NLP Imports
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from textblob import Word
#Bag of Words Support
from sklearn.feature_extraction.text import CountVectorizer
#
#
# Thanks to Goldar, Dreadjak, Bill, thatguy, nosirrahSec, & jferg for the help.
#
#

PYTHONIOENCODING="UTF-8"

def login():
        api = tw.Api(consumer_key = KEYS.CONSUMER_KEY, consumer_secret = KEYS.CONSUMER_SECRET, access_token_key = KEYS.ACCESS_TOKEN_KEY, access_token_secret = KEYS.ACCESS_TOKEN_SECRET, tweet_mode='extended')
        print("\n\nConnected to Twitter\n\n")
        print("Retrieving Tweets...\n")
        if path.exists(directory+'/files.csv') == False:
                userDF = pd.DataFrame(columns=['Times', 'Tweets', 'LD'])
                hopper(api, userDF)
        else:
                userDF = pd.read_csv(os.path.join(directory, 'files.csv'))
                hopper(api, userDF)

def lexical_diversity(text):
        return len(set(text)) / len(text)

def hopper(api, userDF):
        results = api.GetUserTimeline(include_rts=False, count=200, exclude_replies=True)
        for tweet in results:
                fText = tweet.full_text
                fSplit = str(fText.split(' , '))
                tTime = tweet.created_at #Getting the UTC time
                mTime = time.mktime(time.strptime(tTime, "%a %b %d %H:%M:%S %z %Y"))
                eTime = int(mTime)
                ld = lexical_diversity(str(tweet))
                userDF = userDF.append({'Tweets': fSplit, 'Times': eTime, 'LD': ld}, ignore_index=True)
        for index, r in userDF.iterrows():
                tweets=r['Tweets']
                times=r['Times']
                os.chdir(directory)
                fname=str(user)+'_'+str(times)+'.txt'
                corpusfile=open(fname, 'a')
                corpusfile.write(str(tweets))
                tokenized_tweets = sent_tokenize(str(tweets))
                corpusfile.close()
                f1name=str(user)+'.txt'
                userDF = userDF.append({'User': user, 'Tweets': fSplit, 'Times': eTime, 'LD': ld}, ignore_index=True, sort=True)
                userDF = userDF.drop_duplicates()
        userDF = userDF.drop_duplicates(subset=['Times'])
        userDF.to_csv('files.csv')
        print(f"Stats for {user}'s tweets:\n\n")
        ld2 = lexical_diversity(userDF['Tweets'])
        print(f"\nThe Lexical Diversity of {user}'s Tweets is:\t\t\t{ld2}")
        ld3 = np.mean(userDF['LD'])
        print(f"The Statistical Mean Lexical Diversity of {user}'s Tweets is:\t{ld3}")
        ld4 = np.std(userDF['LD'])
        print(f"The StdDev of Lexical Diversity of {user}'s Tweets is:\t\t{ld4}")
        timeStdDev = np.std(userDF['Times'])
        print(f"\n\n{user}'s Tweets occur at this interval:\t\n")
        postInterval = int(timeStdDev)
        print(f"\t{postInterval} seconds apart.\n\n")
        user_languagePreprocessing(api, fSplit, eTime, ld, userDF)

def gonogo(api, fSplit, eTime, ld, userDF):
        gonogo = input("Continue? (Y/N)")
        if gonogo.lower() == 'y':
                print("Sleeping for 4 hours")
                time.sleep(10)
                subsequent(api, directory, fSplit, eTime, ld, userDF)
        else:
                print("Goodbye")
                exit()

def repeater(api, fSplit, eTime, ld, userDF, postInterval):
        sleeping_interval = postInterval-(random.randint(0,480))
        print(f"\t\t\tSleeping for {sleeping_interval} seconds...\t\t\t")
        time.sleep(sleeping_interval)
        subsequent(api, fSplit, eTime, ld, userDF)

def user_languagePreprocessing(api, fSplit, eTime, ld, userDF):
        ps = PorterStemmer()
        bank = []
        stem = []
        lemm = []
        new_userDF = pd.DataFrame(columns=['Times', 'Original', 'Stemmed', 'Lemmerized'])
        print("Beginning NLP Analysis...")
        print("\n")
        userDF= pd.read_csv('files.csv')
        for index, r in userDF.iterrows():
                tweets=r['Tweets']
                tokenized_tweets = word_tokenize(str(tweets))
                for w in tokenized_tweets:
                        if w not in stop_words1:
                                bank.append(w)
        for w in bank:
                rootWord=ps.stem(w)
                stem.append(rootWord)
        for i in bank:
                word1 = Word(i).lemmatize("n")
                word2 = Word(word1).lemmatize("v")
                word3 = Word(word2).lemmatize("a")
                lemm.append(Word(word3).lemmatize())
                new_userDF.append({'Times': eTime, 'Original': tweets, 'Stemmed': rootWord, 'Lemmerized': lemm}, ignore_index=True, sort=True)
        new_userDF = new_userDF.drop_duplicates(subset=['Times'])
        new_userDF.to_csv(os.path.join(directory, 'new_files.csv'))
        bagOWords1(api, fSplit, eTime, ld, userDF)

# Work here
def bagOWords1(api, fSplit, eTime, ld, userDF):
        os.chdir(directory)
        new_userDF = pd.read_csv('new_files.csv')
        for index, r in new_userDF.iterrows():
                tweets=r['Tweets']
                print('Printing data for Original Tweets')
                tweets = [str(tweets)]
                vectorizer.fit(tweets)
                print(vectorizer.vocabulary_)
                vector = vectorizer.transform(tweets)
                print(vector.shape)
                print(type(vector))
                print(vector.toarray())
                bagOWords2(api, fSplit, eTime, ld, userDF)

def bagOWords2(api, fSplit, eTime, ld, userDF):
        for index, r in new_userDF.iterrows():
                stemmed=r['Stemmed']
                print('Printing data for Stemmed Tweets')
                stemmed = [str(stemmed)]
                vectorizer.fit(stemmed)
                print(vectorizer.vocabulary_)
                vector = vectorizer.transform(stemmed)
                print(vector.shape)
                print(type(vector))
                print(vector.toarray())
                bagOWords3(api, fSplit, eTime, ld, userDF)

def bagOWords3(api, fSplit, eTime, ld, userDF):
        for index, r in new_userDF.iterrows():
                lemmerized=r['Lemmerized']
                print('Printing data for Lemmerized Tweets')
                lemmerized = [str(lemmerized)]
                vectorizer.fit(lemmerized)
                print(vectorizer.vocabulary_)
                vector = vectorizer.transform(lemmerized)
                print(vector.shape)
                print(type(vector))
                print(vector.toarray())
        gonogo(api, fSplit, eTime, ld, userDF)

def subsequent(api, ffSplit, eTime, ld, userDF):
        results = api.GetUserTimeline(include_rts=False, count=200, exclude_replies=True)
        print("Retrieving Tweets...")
        print("\n")
        userDF = pd.read_csv('files.csv')
        for tweet in results:
                tweets=userDF['Tweets']
                os.chdir(directory)
                fname=str(user)+'_'+str(times)+'.txt'
                fSplit = str(fText.split(' , '))
                tTime = tweet.created_at #Getting the UTC time
                mTime = time.mktime(time.strptime(tTime, "%a %b %d %H:%M:%S %z %Y"))
                eTime = int(mTime)
                ld = lexical_diversity(str(tweet))
                userDF = userDF.append({'Tweets': fSplit, 'Times': eTime, 'LD': ld}, ignore_index=True, sort=True)
                #user_df(directory, userDF, fSplit, eTime, ld)
                userDF1 = userDF.drop_duplicates(subset=['Times'])
        userDF = userDF1.drop_duplicates(subset=['Times'])
        print('\n\nUpdated Stats for all tweets:\n\n')
        ld2 = lexical_diversity(userDF['Tweets'])
        print(f'\nThe Lexical Diversity of Tweets is:\t\t\t\t\t{ld2}')
        ld3 = np.mean(userDF['LD'])
        print(f'The Updated Statistical Lexical Diversity of Tweets is:\t\t\t{ld3}')
        ld4 = np.std(userDF['LD'])
        print("\n\nTweets occur at this Updated interval:\t\n")
        timeStdDev = np.std(userDF['Times'])
        postInterval = int(timeStdDev)
        print(f"\t{postInterval} seconds apart.\n\n")
        userDF = userDF.drop_duplicates()
        userDF.to_csv('user.csv')
        user_languagePreprocessing(api, fSplit, eTime, ld, userDF)


user = sys.argv[1]
user = user.lower()
directory = os.getcwd()
if os.path.isdir('./files') == False:
        os.makedirs('files')
        directory = directory+'/files'
else:
        directory = directory+'/files'
stop_words1 = set(stopwords.words('english'))
vectorizer = CountVectorizer()
login() 
