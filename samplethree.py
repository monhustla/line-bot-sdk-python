from __future__ import unicode_literals

import os
from os import environ
import sys
import tempfile
import psycopg2
import psycopg2.extras
import logging
import urllib.parse as urlparse
import json
from oauth2client.service_account import ServiceAccountCredentials


from flask import Flask, request, abort
#from waitress import serve
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

from utils import logcall, logcall_always
from Mc3 import Mc3

app = Flask(__name__)


line_bot_api = LineBotApi(os.environ['channel_secret'])
handler = WebhookHandler(os.environ['handler'])
parser = WebhookParser(os.environ['handler'])











@app.route("/callback", methods=['POST'])
@logcall_always
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handle_callback(body, signature)
    except Exception as ex:
        logging.exception("An error occured in callback handler")

    return 'ok'
    

@logcall
def handle_callback(body, signature):
    # handle webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    for event in events:
        
           
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        handle_message_event(event)

@logcall
def handle_message_event(event):
        
        eventText=event.message.text.lower()
        eventTextLower = eventText.rstrip()
        
        if "vbot" in eventTextLower:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="ha"))
            return

        if not eventTextLower.startswith(Mc3.trigger.lower()):
            # this is not an Mc3 event so keep going.
            return
        else:
            # verify that event is one we are interested in.
            print("Processing Message: " + eventText)

            # remove the trigger from the line and pass it to the handler
            eventArgs = eventText[ len(Mc3.trigger) : ]
        
            mc3 = Mc3(line_bot_api, event)
            
            #I need help understanding this. It seems like all commands now must have mc3 for some reason.
            #There is an easter egg I want that does not contain 'mc3'.-TLT
            
            
            # if we process the command then keep going 
            # otherwise fall through to the old handlers
            try:
                if mc3.process(eventArgs):
                    return
            except Exception as ex:
                logging.exception("An error occured handeling command " + eventArgs)
                return
                
        
        
         
                    

        if eventTextLower == "mc3 og vision lol":
            line_bot_api.reply_message(
                event.reply_token,
                VideoSendMessage(
                    original_content_url='https://dl.dropboxusercontent.com/s/hiak83i7qzr7p5a/og%20vision.mp4',
                    preview_image_url='https://dl.dropboxusercontent.com/s/hiak83i7qzr7p5a/og%20vision.mp4'))

        if eventTextLower == "mc3 sig_calculator":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="To use the sig calculator, simply type in 'Mc3 sig (champname) (sig level)'."+'\n'+'\n'+
                                "Here is an example:"+'\n'+
                                "'Mc3 sig drax 50'"))            
                                        
        
            
        if eventTextLower == "mc3 interactive maps":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="http://marveltrucos.x10.mx/coc/aq/"))
            

            
        #AW Command Tree
        if eventTextLower == "mc3 aw":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/ZxgWTY7.jpg',
                    preview_image_url='https://i.imgur.com/ZxgWTY7.jpg'))
            

        
      

                #Duels Keywords
        if eventTextLower == "mc3 sparring":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Created by Royal Marshall:"+'\n'+
                               "https://docs.google.com/spreadsheets/d/1zWmsazuyPTQEEc6RI3dDQSjDI5gF-HM-PpvLLtJZCHk/htmlview"))            
          
        
        
        
            
       
     

            
        if eventTextLower == "mc3 line cutoffs":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="To use to the line arena cutoff tool type 'Mc3 cutoffs (champname)'"+'\n'+
                               "Example: Mc3 cutoffs gwenpool"))    
                
        #Special Quest Command Tree
        if eventTextLower == "mc3 special quests":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="rol guide"+'\n'+"rttl guide"+'\n'+"lol"))
            #Special Quest Keywords
                #Lol Command Tree
        if eventTextLower == "mc3 lol":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="lol map"+'\n'+"lol fights"))
        if eventTextLower == "mc3 lol map":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/vB3Ix7L.jpg',
                    preview_image_url='https://i.imgur.com/vB3Ix7L.jpg'))
        if eventTextLower == "mc3 lol fights":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="To pull up lol fights type:'Mc3 lolfight (champname)'"+'\n'+"Example:"+'\n'+"'Mc3 lolfight agentvenom'"))            
        if eventTextLower == "mc3 rol guide":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Coming Soon"))
        if eventTextLower == "mc3 rttl guide":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="https://drive.google.com/file/d/0B4ozoShtX2kFcDV4R3lQb1hnVnc/view?pref=2&pli=1"))
        
         

            
 
                        
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
    
