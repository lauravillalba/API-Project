from flask import request
from pymongo import MongoClient
import pandas as pd
from bson.json_util import loads
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from config import LOCAL_DB


# Connect to the database
client = MongoClient(LOCAL_DB)
db = client.get_database()
coll_users = db['users']
coll_scenes = db['scenes']
coll_dialogues = db['dialogues']


def sentimentAnalysis(scenename, df):
    #Devuelve el sentiment de cada frase de la escena, calcula la media de sentiment de la escena y la incluye en coll_scenes:
    sia = SentimentIntensityAnalyzer()
    lista_compound = []
    if 'dialog' in list(df.columns):
        for e in df.dialog:
            lista_compound.append(sia.polarity_scores(e)['compound'])
    
    df['compound'] = lista_compound
    return df
