from flask import Flask, request
from sklearn.feature_extraction.text import CountVectorizer
import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity as distance
import api_get as get
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/api_db")
db = client.get_database()
coll_users = db['users']
coll_scenes = db['scenes']
coll_dialogues = db['dialogues']

@app.route('/recommended/<personaje>', methods=['GET'])
def recommended (personaje):
    #Consulto todos los nombres de los personajes:
    names = get.usersNames()
    characters = []
    for n in names:
        characters.append(n['userName'])
    characters = characters[1:]

    #Creo un diccionario vacío donde guardar los diálogos de cada personaje:
    big_dict = {}
    for c in characters:
        dialogues = pd.DataFrame(get.characterDialogues(c))
        lista = []
        if 'dialog' in list(dialogues.columns):
            for d in dialogues['dialog']:
                lista.append(d)
            big_dict[c] = ' '.join(lista)

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
    query = {'$and': [{'userNames': {'$eq':'joy'}},{'sceneID':{'$ne': 0}}]}
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

app.run("0.0.0.0", 2020, debug=True)