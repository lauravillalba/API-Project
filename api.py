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


@app.route('/addUser/',methods=['POST'])
def newUser ():    
    
    #Add new user to coll_users:
    name = request.form.get('name')
    equal_name = coll_users.distinct("userName")
    if name in equal_name:
        return "Ya existe ese nombre"
    
    else:
        dict_addUser = {
                        'userName':name
        }
        coll_users.insert_one(dict_addUser)

    return f"Usuario '{name}' creado!"

@app.route('/addScene/',methods=['POST'])
def newScene():
    #Add new scene to coll_scenes:
    scene = request.form.get('scene')
    name = request.form.getlist('name')
    equal_scene =coll_scenes.distinct("sceneName")
    if scene in equal_scene:
        return "Esta escena ya existe"
    else:
        dict_addScene={
                        'sceneName': scene,
                        'userName': name
        }
        coll_scenes.insert_one(dict_addScene)

    return f"Escena '{scene}' creada!"

@app.route('/addDialog/',methods=['POST'])
def newDialog():
    #Add new dialog to coll_dialogs:
    name = request.form.get('name')
    scene = request.form.get('scene')
    dialog = request.form.getlist('dialog')
    nameInScene= list(coll_scenes.find({"$and": [{"sceneName":scene},{"userName":name}]}))
    if name not in nameInScene:
        return f"La escena {scene} o el nombre {name} no son correctos."
    else:
        dict_addDialog={
                        'sceneName':scene,
                        'userName':name,
                        'dialog': dialog 
        }
        coll_dialogues.insert_one(dict_addDialog)
    return "Dialogo guardado!"

app.run("0.0.0.0", 2020, debug=True)
