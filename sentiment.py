from bson.json_util import dumps
from pymongo import MongoClient

def sentimentAnalysis(scenename):
    
    
    return dumps(coll_dialogues.find({'sceneName': scenename}, {'_id': 0, 'userID':1, 'userName':1,'sceneID':1, 'sceneName':1, 'dialogID':1, 'dialog':1}))