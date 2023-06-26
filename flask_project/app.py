import os
import requests
import json
from flask import Flask, request, render_template, redirect, url_for

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'app/templates')
static_path = os.path.join(project_root, 'app/static')
app = Flask(__name__, template_folder= 'Template')
context_set = ""

@app.route('/', methods = ['POST', 'GET'])
def index():
 if request.method == 'GET':
   val = ''
   val = str(request.args.get('text'))
   if val != 'None':
        data = json.dumps({"sender": "Rasa","message": val})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://18.220.35.8:5005/webhooks/rest/webhook', data= data, headers = headers)
        res = res.json()
        print(res)
        val = res[0]['text']
        return val
   return render_template('index.html')

@app.route('/rasa_response', methods = ['POST', 'GET'])
def rasa_reponse():
    if request.method == 'GET':
        val = str(request.args.get('text'))
        data = json.dumps({"sender": "Rasa","message": val})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data= data, headers = headers)
        res = res.json()
        print(res)
        val = " "
        for r in res:
          val = val+r['text']
        return val


        

application = app