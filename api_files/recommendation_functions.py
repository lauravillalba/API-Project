from flask import request
import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity as distance
from sklearn.feature_extraction.text import CountVectorizer
from pymongo import MongoClient
from config import LOCAL_DB



# Connect to the database
client = MongoClient(LOCAL_DB)
print(LOCAL_DB)
db = client.get_database()
coll_users = db['users']
coll_scenes = db['scenes']
coll_dialogues = db['dialogues']


def listaPersonajes (names):
    #Lista con todos los nombres de los personajes:
    characters = []
    for n in names:
        characters.append(n['userName'])
    characters = characters[1:]
    return characters

def recomendedCharacter(personaje, big_dict):
    #Analizo las frases de cada personaje:
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(big_dict.values())
    matrix = sparse_matrix.todense()
    df = pd.DataFrame(matrix, 
                    columns=count_vectorizer.get_feature_names(), 
                    index=big_dict.keys())

    similarity_matrix = distance(df,df)
    sim_df = pd.DataFrame(similarity_matrix, columns=big_dict.keys(), index=big_dict.keys())

    #Creo ranking del personaje consultado:
    ranking = (pd.DataFrame(sim_df[personaje][1:].sort_values(ascending = False))).index

    #Consulta a la API para listar con quién tiene diálogos este personaje:
    query = {'$and': [{'userNames': {'$eq':personaje}},{'sceneID':{'$ne': 0}}]}
    with_character = list(coll_scenes.find(query,{'_id':0,'userNames':1}))

    comunes = []
    for e in with_character:
        comunes.append(e['userNames'])
    comunes = list(set([e for b in comunes for e in b]))

    #Verificación (comprobar con quién no comparte diálogo) y recomendación:
    for e in ranking:
        if e not in comunes:
            return(f'Recomendamos a {e}')

    return f"No hay recomendación para el personaje {personaje}"
