from flask import Flask, request
import json
import requests
import os
import sys
import errno
import os
import sys
import tempfile
from argparse import ArgumentParser


from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)
 
app = Flask(__name__)

line_bot_api = LineBotApi('jCCJTBH9PKP0UzrCtVCpT99E2kOPn3bowhUA8KX1hcxMHwqdZbfLzP/I6leONvKqZmNyqKC1w/2pZYau7cKtSQePM/Wb+Vj8t3F9XbyRavOLgd/1Y6PUccEc5/8ce/BJjGcGlHH0T/7l2nUlpqsAIgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2f8bf1b9951192d713bc216bdc585df2')

new=open("userids.txt","w")

@app.route('/')
def index():
    return "Hello World!"

@app.route('/callback', methods=['POST'])
def callback():
    json_line = request.get_json()
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    user = decoded['events'][0]['source']['userId']
    #id=[d['replyToken'] for d in user][0]
    #print(json_line)
    with open("userids.txt",'w') as outfile:
        json.dump(user,outfile)
    
    print("ok",user)
    print (user)
    return '',200
    
@app.route

 
def sendText(user, text):
    LINE_API = 'https://api.line.me/v2/bot/message/multicast'
    Authorization = 'jCCJTBH9PKP0UzrCtVCpT99E2kOPn3bowhUA8KX1hcxMHwqdZbfLzP/I6leONvKqZmNyqKC1w/2pZYau7cKtSQePM/Wb+Vj8t3F9XbyRavOLgd/1Y6PUccEc5/8ce/BJjGcGlHH0T/7l2nUlpqsAIgdB04t89/1O/w1cDnyilFU='
 
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }
    data = user
    new=open("userids.txt","w")
    z=str(user)
    new.write(z)
    print(z)
    new.close()
    
 
 
    r = requests.post(LINE_API, headers=headers, data=data) 
    #print(r.text)



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
