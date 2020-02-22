from flask import Flask, request
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

# Connect to the database
client = MongoClient("mongodb://localhost:27017/api_db")
db = client.get_database()
coll_users = db['users']
coll_scenes = db['scenes']
coll_dialogues = db['dialogues']

@app.route('/usersnames/',methods=['GET'])
def usersNames():
    #Devuelve los nombre e id de todos los personajes
    return dumps(coll_users.find({},{'_id': 0, 'userName':1, 'userID':1}))

@app.route('/scenescharacter/<character>', methods=['GET'])
def scenesCharacter(character):
    #Devuelve las escenas en las que sale un personaje
    return dumps(coll_scenes.find({'userNames':character}, {'_id': 0, 'sceneID':1, 'sceneName':1}))

@app.route('/sceneinfo/<scenename>', methods=['GET'])
def sceneInfo(scenename):
    #Devuelve  nombre, id y personajes de una escena
    return dumps(coll_scenes.find({'sceneName':scenename}, {'_id': 0, 'sceneID':1, 'sceneName':1, 'userNames':1}))

@app.route('/scenedialogues/<scenename>', methods=['GET'])
def sceneDialogues(scenename):
    #Devuelve los diálogos de una escena y el personaje que lo ha dicho
    return dumps(coll_dialogues.find({'sceneName': scenename}, {'_id': 0, 'userID':1, 'userName':1,'sceneID':1, 'sceneName':1, 'dialogID':1, 'dialog':1}))

@app.route('/characterdialogues/<character>', methods=['GET'])
def characterDialogues(character):
    #Devuelve todos los diálogos de un personaje y la escena donde los dice
    return dumps(coll_dialogues.find({'userName': character}, {'_id': 0, 'userID':1, 'userName':1,'sceneID':1, 'sceneName':1, 'dialogID':1,'dialog':1}))


@app.route('/scene/<scenename>/sentiment', methods=['GET'])
def sentimentScene(scenename):
    return "BLA"


app.run("0.0.0.0", 2020, debug=True)