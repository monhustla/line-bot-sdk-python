from __future__ import unicode_literals
import os
from os import environ
import sys
import tempfile
import psycopg2
import psycopg2.extras
import urllib.parse as urlparse
import json
from oauth2client.service_account import ServiceAccountCredentials
from openpyxl import Workbook, load_workbook

from flask import Flask, request, abort
from argparse import ArgumentParser

import requests

from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
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
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent, ImageSendMessage,VideoSendMessage
)

from Mc3 import Mc3

app = Flask(__name__)


line_bot_api = LineBotApi(os.environ['channel_secret'])
handler = WebhookHandler(os.environ['handler'])

line_bot_api = LineBotApi(os.environ['channel_secret'])
parser = WebhookParser(os.environ['handler'])

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )


def get_prestige_for_champion(champ, sig):
    cur = None
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""SELECT prestige FROM prestige_table WHERE champ = %(champ)s AND sig = %(sig)s""", {"champ": champ, "sig": sig})
        rows = cur.fetchall()
        for row in rows:
            return str(row['prestige'])                           # Returns a prestige value
        else:
            return None                                           # Returns None if a champ or sig wasn't found
    except psycopg2.Error:
        conn.rollback()
        print("PostgreSQL Error: " + e.diag.message_primary)
        pass
    finally:
        if cur is not None:
            cur.close()


            
def calculate_prestige(champs):
    if champs is None:
        return 0

    # if champs isn't a dict, it might still be a JSON string
    if not type(champs) is dict:
        champs = json.loads(champs)

    # Ok, here's a little one-liner wonder:
    #    First, we sort the array in descending order
    #    Then, we slice off the first 5 elements (if there are that many)
    top_champs = sorted(champs.values(), reverse=True)[:5]
    results = list(map(int, top_champs)) 
    top_champcount=len(top_champs)
    top_champamount=sum(results)
    average=(int(top_champamount/top_champcount))
    return (str(average))

def alliance_prestige(players):
    if players is None:                                            # can't calculate a prestige from nothing, prevents a divide by 0 error
        return 0

    # if champs isn't a dict, it might still be a JSON string
    if not type(players) is dict:
        players = json.loads(players)

    # Ok, here's a little one-liner wonder:
    #    First, we sort the array in descending order
    #    Then, we slice off the first 5 elements (if there are that many)
    top_players = sorted(players.values(), reverse=True)[:30]
    results = list(map(int, top_players)) 
    top_playercount=len(top_players)
    top_playeramount=sum(results)
    alliancep=str(int(top_playeramount/top_playercount)) 

    # And grab the average (as an integer since all inputs are integers
    # It has a precision of 1 so converting to int again will remove the trailing 0) e.g. 1234.0
    return (alliancep)

def isValidCommand(command):
    return command in commands

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    return handle_callback(body, signature)
    


def handle_callback(body, signature):

    # handle webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
        
        print (events)

    for event in events:
           
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        
        
        eventText=event.message.text    

        

        # verify that event is one we are interested in.
        if eventText.startswith(Mc3.trigger):
            
            
            
            
            
            
            # remove the trigger from the line and pass it to the handler
            eventArgs = eventText[ len(Mc3.trigger) : ]
        
            mc3 = Mc3(line_bot_api, event)

            # if we process the command then keep going 
            # otherwise fall through to the old handlers
            if mc3.process(eventArgs):
                continue
                

        eventText=event.message.text
        trigger = "Mc3 yay"
        if eventText.startswith(trigger):
            
            fuck=event.message.user_id
            print(fuck)
            print (user)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="ok"))
            
                 
 
        

    return 'ok'
            
            
 
            
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
