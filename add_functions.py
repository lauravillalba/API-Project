from flask import request
from pymongo import MongoClient


# Connect to the database
client = MongoClient("mongodb://localhost:27017/api_db")
db = client.get_database()
coll_users = db['users']
coll_scenes = db['scenes']
coll_dialogues = db['dialogues']


def addUser (name):
    #Add new user to coll_users:
    name = request.form.get('name')
    n_user = max(coll_users.distinct('userID'))+1
    equal_name = coll_users.distinct('userName')
    if name in equal_name:
        return "Ya existe ese nombre"
    
    else:
        dict_addUser = {
                        'userID': n_user,
                        'userName':name,
                        'userSentiment':0
        }
        coll_users.insert_one(dict_addUser)

    return f"Usuario '{name}' creado --> id: {n_user}!"

def addScene(scene,names):
    #Add new scene to coll_scenes:
    scene = request.form.get('scene')
    n_scene = max(coll_scenes.distinct('sceneID'))+1
    names = request.form.getlist('names')
    equal_scene =coll_scenes.distinct("sceneName")
    if scene in equal_scene:
        return "Esta escena ya existe"
    else:
        dict_addScene={
                        'sceneID':n_scene,
                        'sceneName': scene,
                        'sceneSentiment': 0,
                        'userNames': names
        }
        coll_scenes.insert_one(dict_addScene)

    return f"Escena '{scene}' creada --> id: {n_scene}"

def addDialog(scene,name,dialog):
    #Add new dialog to coll_dialogs:
    scene = request.form.get('scene')
    n_scene = list(coll_scenes.find({'sceneName':scene}))
    name = request.form.get('name')
    n_user = list(coll_users.find({'userName':name}))
    dialog = request.form.get('dialog')
    n_dialog = max(coll_dialogues.distinct('dialogID'))+1
    nameInScene= list(coll_scenes.find({"$and": [{"sceneName":scene},{"userNames":name}]}))
    
    if not nameInScene or name not in nameInScene[0]['userNames']:
        return f"La escena {scene} o el nombre {name} no son correctos."
    else:
        dict_addDialog={
                        'sceneName':scene,
                        'sceneID':n_scene[0]['sceneID'],
                        'userName':name,
                        'userID': n_user[0]['userID'],
                        'dialog': dialog,
                        'dialogID': n_dialog
        }
        coll_dialogues.insert_one(dict_addDialog)
    print (dict_addDialog['sceneID'],dict_addDialog['dialog'])
    return f"Dialogo guardado --> id: {n_dialog}!"