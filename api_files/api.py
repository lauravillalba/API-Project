from flask import Flask, request
from pymongo import MongoClient
from bson.json_util import dumps, loads
import requests
import pandas as pd
from recommendation_functions import listaPersonajes, recomendedCharacter
from add_functions import addUser, addScene, addDialog
from sentiment_functions import sentimentAnalysis
from config import LOCAL_DB, PORT

app = Flask(__name__)

# Connect to the database

client = MongoClient(LOCAL_DB)
db = client.get_database()
coll_users = db['users']
coll_scenes = db['scenes']
coll_dialogues = db['dialogues']

#-------------------------------------------------- POST ------------------------------------------------------------------

@app.route('/addUser/',methods=['POST'])
def newUser ():
    #Add new user to coll_users:

    return addUser ('name')

@app.route('/addScene/',methods=['POST'])
def newScene():
    #Add new scene to coll_scenes:

    return addScene('scene','names')

@app.route('/addDialog/',methods=['POST'])
def newDialog():
    #Add new dialog to coll_dialogs:
    
    return addDialog('scene','name','dialog')

#-------------------------------------------------- GET ------------------------------------------------------------------
@app.route('/usersnames/',methods=['GET'])
def usersNames():
    #Devuelve los nombre e id de todos los personajes
    return dumps(coll_users.find({},{'_id': 0, 'userName':1, 'userID':1, 'userSentiment':1}))


@app.route('/character/<character>',methods=['GET'])
def characterDetails(character):
    #Devuelve los detalles del personaje consultado
    return dumps(coll_users.find({'userName':character},{'_id': 0, 'userName':1, 'userID':1, 'userSentiment':1}))


@app.route('/scenescharacter/<character>', methods=['GET'])
def scenesCharacter(character):
    #Devuelve las escenas en las que sale un personaje
    return dumps(coll_scenes.find({'userNames':character}, {'_id': 0, 'sceneID':1, 'sceneName':1, 'sceneSentiment':1}))


@app.route('/sceneinfo/<scenename>', methods=['GET'])
def sceneInfo(scenename):
    #Devuelve nombre, id y personajes de una escena
    return dumps(coll_scenes.find({'sceneName':scenename}, {'_id': 0, 'sceneID':1, 'sceneName':1, 'userNames':1, 'sceneSentiment':1}))


@app.route('/scenedialogues/<scenename>', methods=['GET'])
def sceneDialogues(scenename):
    #Devuelve los diálogos de una escena y el personaje que lo ha dicho
    return dumps(coll_dialogues.find({'sceneName': scenename}, {'_id': 0, 'userID':1, 'userName':1,'sceneID':1, 'sceneName':1, 'dialogID':1, 'dialog':1}))


@app.route('/characterdialogues/<character>', methods=['GET'])
def characterDialogues(character):
    #Devuelve todos los diálogos de un personaje y la escena donde los dice
    return dumps(coll_dialogues.find({'userName': character}, {'_id': 0, 'userID':1, 'userName':1,'sceneID':1, 'sceneName':1, 'dialogID':1,'dialog':1}))


#-------------------------------------------------- SENTIMENT ------------------------------------------------------------------

@app.route('/sentimentscene/<scenename>', methods=['GET'])
def sentimentScene(scenename):
    #Devuelve el sentiment de cada frase de la escena y calcula la media de sentiment de la escena y la incluye en coll_scenes (por defecto 0)
    df_scene = pd.DataFrame(loads(sceneDialogues(scenename)))
    df = sentimentAnalysis('scenename',df_scene)
    
    #Actualizo sentiment mean a la escena (se crea como 0 por defecto):
    coll_scenes.update_one({'sceneName': scenename}, {'$set': {'sceneSentiment':df['compound'].mean()}})
    return df.to_json(orient = 'records',force_ascii=False)


@app.route('/sentimentcharacter/<character>', methods=['GET'])
def sentimentCharacter(character):
    #Devuelve el sentiment de un personaje a partir de todas las frases que haya dicho
    df_dialogues=pd.DataFrame ( loads(characterDialogues(character)))
    df = sentimentAnalysis('character',df_dialogues)
    
    #Actualizo sentiment mean del personaje (se crea con valor 0 por defecto):   
    coll_users.update_one({'userName': character}, {'$set': {'userSentiment':df['compound'].mean()}})
    return dumps(characterDetails(character))


#-------------------------------------------------- RECOMMENDATION ------------------------------------------------------------------

@app.route('/recommended/<personaje>', methods=['GET'])
def recommending(personaje):
    
    #Consulto todos los nombres de los personajes:
    names = loads(usersNames())
    characters = listaPersonajes (names)

    #Creo un diccionario vacío donde guardar los diálogos de cada personaje:
    big_dict = {}
    for c in characters:
        dialogues = pd.DataFrame(loads(characterDialogues(c)))
        lista = []
        if 'dialog' in list(dialogues.columns):
            for d in dialogues['dialog']:
                lista.append(d)
            big_dict[c] = ' '.join(lista)

    return recomendedCharacter(personaje, big_dict)


app.run('0.0.0.0', port=PORT, debug=True)