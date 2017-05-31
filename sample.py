from flask import Flask, request
import json
import requests
import os
import sys
 
app = Flask(__name__)
 
@app.route('/')
def index():
    return "Hello World!"

@app.route('/callback', methods=['POST'])
def callback():
    json_line = request.get_json()
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    user = decoded["userId"]
    #id=[d['replyToken'] for d in user][0]
    #print(json_line)
    print("ok",user)
    sendText(user,'ok') 
    return '',200
 
def sendText(user, text):
    LINE_API = 'https://api.line.me/v2/bot/message/multicast'
    Authorization = 'jCCJTBH9PKP0UzrCtVCpT99E2kOPn3bowhUA8KX1hcxMHwqdZbfLzP/I6leONvKqZmNyqKC1w/2pZYau7cKtSQePM/Wb+Vj8t3F9XbyRavOLgd/1Y6PUccEc5/8ce/BJjGcGlHH0T/7l2nUlpqsAIgdB04t89/1O/w1cDnyilFU='
 
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }
    data = json.dumps(user)
    
 
    
    r = requests.post(LINE_API, headers=headers, data=data) 
    #print(r.text)
 

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
