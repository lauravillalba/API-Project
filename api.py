from flask import Flask, request
from mongoconnect import getCompanyWithName


app = Flask(__name__)

@app.route('/hola')
def hello():
    pepe = {
        "nombre": "Luis",
        "edad": 30
    }
    return pepe

@app.route('/company/<name>')
def getCompany(name):
    return getCompanyWithName(name)

app.run("0.0.0.0", 2020, debug=True)
