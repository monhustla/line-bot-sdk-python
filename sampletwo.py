from __future__ import unicode_literals
import os
from os import environ
import sys
import tempfile
import psycopg2
import urllib.parse as urlparse
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent, ImageSendMessage
)




app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('MyProject-3164a19e689c.json', scope)
gc = gspread.authorize(credentials)

line_bot_api = LineBotApi('jCCJTBH9PKP0UzrCtVCpT99E2kOPn3bowhUA8KX1hcxMHwqdZbfLzP/I6leONvKqZmNyqKC1w/2pZYau7cKtSQePM/Wb+Vj8t3F9XbyRavOLgd/1Y6PUccEc5/8ce/BJjGcGlHH0T/7l2nUlpqsAIgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2f8bf1b9951192d713bc216bdc585df2')


line_bot_api = LineBotApi('jCCJTBH9PKP0UzrCtVCpT99E2kOPn3bowhUA8KX1hcxMHwqdZbfLzP/I6leONvKqZmNyqKC1w/2pZYau7cKtSQePM/Wb+Vj8t3F9XbyRavOLgd/1Y6PUccEc5/8ce/BJjGcGlHH0T/7l2nUlpqsAIgdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('2f8bf1b9951192d713bc216bdc585df2')


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





@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
        
    for event in events:
        if isinstance(event, JoinEvent):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Hey, thank you for inviting the MCOC Concierge In-Chat Bot. All commands need to be prefaced with: Mc3. To get started type: Mc3 list'))
           
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue            
        if event.message.text=="Mc3 save profile":
            json_line = request.get_json()
            json_line = json.dumps(json_line)
            decoded = json.loads(json_line)
            user = decoded['events'][0]['source']['userId']
            f=str(user)
            profile= line_bot_api.get_profile(user)
            name=(profile.display_name)
            print(f)
            cur=conn.cursor()
            cur.execute("INSERT INTO prestige_data (lineid, summoner_name, champ_data) VALUES (%s, %s, %s);""",
                        (f, name, "whocares"))
            cur.execute("SELECT lineid, summoner_name, champ_data FROM prestige_data""")
            rows = cur.fetchall()
            
            
            for row in rows:
                print("    LINE ID: " + row[0] + "\n")
                print("    Summoner: " + row[1] + "\n")
                
        if "Mc3 input champ1:" in event.message.text:
            s1=event.message.text
            s2=":"
            s3="*"
            champ=s1[s1.find(s2)+1 : s1.find(s3)]
            sig=(s1[s1.index(s3) + len(s3):])
            champ1=str(champ)
            print(champ1)
            print (sig)
            sig1=int(sig)
            json_line = request.get_json()
            json_line = json.dumps(json_line)
            decoded = json.loads(json_line)
            user = decoded['events'][0]['source']['userId']
            f=str(user)
            profile= line_bot_api.get_profile(user)
            name=(profile.display_name)
            cur=conn.cursor()
            cur.execute("SELECT * FROM prestige where stars_champ_rank=%(stars_champ_rank)s",{"stars_champ_rank":champ1})
            rows=cur.fetchall()
            for row in rows:
                h=str(row[sig1])
            cur=conn.cursor()
            cur.execute("""INSERT INTO prestige_data(lineid, summoner_name, champ_data),
               VALUES(f, '~~~Nilpo~~~', '{}'
               ON CONFLICT (lineid)
               DO UPDATE SET summoner_name = Excluded.summoner_name, champ_data = Excluded.champ_data;""")
            cur.execute("""INSERT INTO prestige_data(lineid, summoner_name, champ1_name, champ1_prestige, champ2_name, champ2_prestige, champ3_name, champ3_prestige, champ4_name, champ4_prestige, champ5_name, champ5_prestige) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,);""",
                        (f, name, champ, h, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',))

            rows=cur.fetchall()
            for row in rows:
                h=str(row[sig1])
                print (h)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=h))
            #profile= line_bot_api.get_profile(user)
            #name=(profile.display_name)
            #cur=conn.cursor()
            #cur.execute("""INSERT INTO prestige_data (lineid, summoner_name, champ_data) VALUES (%s, %s, %s);""",
            #(f, name, data))
            #cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid= %(lineid)s""",
             #           {"lineid":f})
            #rows = cur.fetchall()
            #for row in rows:
              #  g=("Summoner: " + row[1] + "\n")
               # line_bot_api.reply_message(
                #    event.reply_token,
                 #   TextSendMessage(text=content))
                
        if event.message.text=="Mc3 my name":
            json_line = request.get_json()
            json_line = json.dumps(json_line)
            decoded = json.loads(json_line)
            user = decoded['events'][0]['source']['userId']
            f=str(user)
            profile= line_bot_api.get_profile(user)
            name=(profile.display_name)
            cur=conn.cursor()
            cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid= %(lineid)s""",
                        {"lineid":f})
            rows= cur.fetchall()
            for row in rows:
                h=("Summoner: " + row[1] + "\n")
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=h))
                                
                
                
                   
                        
                        
        #Whole List Breakdown    
        if event.message.text == "Mc3 list":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="aq"+'\n'+"aw"+'\n'+"arena"+'\n'+"calendars"+'\n'+"duels"+'\n'+"masteries"+'\n'+"prestige"+'\n'+"special quests"+'\n'+"synergies"))     
        
        #Specific List Breakdown, make sure to follow the headers identifying the class.
            #Aq Trigger
        if event.message.text == "Mc3 aq":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="boss practice"+'\n'+"aq costs"+'\n'+"aq maps"+'\n'+"aq rewards"))
            
                #aq maps tree
        if event.message.text == "Mc3 aq maps":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="interactive maps"+'\n'+"map 3"+'\n'+"map 4"+'\n'+"map 5"+'\n'+"map 6"))            
        
         #AQ Keywords
        if event.message.text == "Mc3 aq costs":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/BvLSyYt.jpg',
                    preview_image_url='https://example.com/preview.jpg'
                )
            )
                    
        if event.message.text == "Mc3 aq rewards":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/ZwdRIoj.jpg',
                    preview_image_url='https://example.com/preview.jpg'
                )
            )
            
        if event.message.text == "Mc3 boss practice":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/71x09Rm.jpg',
                    preview_image_url='https://example.com/preview.jpg'
                )
            )
            
        if event.message.text == "Mc3 interactive maps":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="http://marveltrucos.x10.mx/coc/aq/"))
            
        if event.message.text == "Mc3 map 3":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/GZYgvhS.jpg',
                    preview_image_url='https://example.com/preview.jpg'))
            
        if event.message.text == "Mc3 map 4":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Coming soon")) 
            
        if event.message.text == "Mc3 map 5":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/TqTHnKB.jpg',
                    preview_image_url='https://example.com/preview.jpg'))
            
        if event.message.text == "Mc3 map 6":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/Eie596I.jpg',
                    preview_image_url='https://example.com/preview.jpg'))
            
        #AW Command Tree
        if event.message.text == "Mc3 aw":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="aw map"))
            
            #AW Keywords    
        if event.message.text == "Mc3 aw map":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/ZxgWTY7.jpg',
                    preview_image_url='https://example.com/preview.jpg'))
        
        #Arena Command Tree
        if event.message.text == "Mc3 arena":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="t4b"+'\n'+"basic"+'\n'+"cutoffs"))            
            #Arena Keywords   
        if event.message.text == "Mc3 basic":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/LWHaCCv.jpg',
                    preview_image_url='https://example.com/preview.jpg'))
        if event.message.text == "Mc3 t4b":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/EwC1hdp.jpg',
                    preview_image_url='https://example.com/preview.jpg'))
        if event.message.text == "Mc3 cutoffs":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="https://docs.google.com/spreadsheets/d/1sJtSVnjhhRNxpiuMR5uXrsTlrsXMjp9TNO7JHDXhtsk/htmlview"))

        #Calendar Command Tree
        if event.message.text == "Mc3 calendars":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="daily rotation calendar"+'\n'+"monthly calendar"+'\n'+"premium schedule"+'\n'+"basic schedule"))
            #Calendar Keywords    
        if event.message.text == "Mc3 daily rotation calendar":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/iyNbSOk.jpg',
                    preview_image_url='https://example.com/preview.jpg'))            
        if event.message.text == "Mc3 monthly calendar":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Coming Soon"))
        if event.message.text == "Mc3 premium schedule":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="http://marveltrucos.x10.mx/premium.php"))
        if event.message.text == "Mc3 basic schedule":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="http://marveltrucos.x10.mx/basics.php"))
        
        #Duels Command Tree
        if event.message.text == "Mc3 duels":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="duel targets"))
                #Duels Keywords
        if event.message.text == "Mc3 duel targets":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="https://docs.google.com/spreadsheets/d/1FZdJPB8sayzrXkE3F2z3b1VzFsNDhh-_Ukl10OXRN6Q/edit#gid=1544272893"))            
          
        
        #Masteries Command Tree
        if event.message.text == "Mc3 masteries":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="ronin nupe"+'\n'+"mastery costs"+'\n'+"mastery builder"+'\n'+"mastery pi"))
                #Masteries Keywords
        if event.message.text == "Mc3 ronin nupe":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="https://docs.google.com/document/d/1iC2YjlXa8PNsBGHiupLV6lsdXj7wnH1bC2l-HIWOiwI/edit"))
        if event.message.text == "Mc3 mastery cost":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/Mc3aao5.jpg',
                    preview_image_url='https://example.com/preview.jpg'))           
        if event.message.text == "Mc3 mastery builder":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="https://alsciende.github.io/masteries/v10.0.1/#0000000000000000000000000000000000000010000000000000000"))            
        if event.message.text == "Mc3 mastery pi":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/T12L38x.jpg',
                    preview_image_url='https://example.com/preview.jpg'))          
            
            
        #Prestige Command Tree
        if event.message.text == "Mc3 prestige":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="prestige calculator"+'\n'+"prestige list"))         
            #Prestige Keywords
        if event.message.text == "Mc3 prestige calculator":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="https://docs.google.com/spreadsheets/d/1YdOWdX2zpyWBBLos36CthqpJ9y1HlPdSHV8jtvkeF3E/copy"))
        if event.message.text == "Mc3 prestige list":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="https://docs.google.com/spreadsheets/d/1Cd3-X2lAQyJBlBuxBld6fsWBw4HkBdm2AFybHk3nfS4/pubhtml#"))  
            
        #Special Quest Command Tree
        if event.message.text == "Mc3 special quests":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="rol guide"+'\n'+"rttl guide"+'\n'+"lol"))
            #Special Quest Keywords
                #Lol Command Tree
        if event.message.text == "Mc3 lol":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="lol map"+'\n'+"lol fights"))
        if event.message.text == "Mc3 lol map":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/vB3Ix7L.jpg',
                    preview_image_url='https://example.com/preview.jpg'))
        if event.message.text == "Mc3 lol fights":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Coming Soon"))            
        if event.message.text == "Mc3 rol guide":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Coming Soon"))
        if event.message.text == "Mc3 rttl guide":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="https://drive.google.com/file/d/0B4ozoShtX2kFcDV4R3lQb1hnVnc/view?pref=2&pli=1")) 

            
        #Synergies Command Tree    
        if event.message.text == "Mc3 synergies":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="attack teams"+'\n'+"bleed teams"+'\n'+"crit teams"+'\n'+"power gain teams")) 
            #Synergies Keywords   
        if event.message.text == "Mc3 attack teams":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/WTyyl7t.jpg',
                    preview_image_url='https://example.com/preview.jpg'))
        if event.message.text == "Mc3 bleed teams":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Coming Soon"))
        if event.message.text == "Mc3 crit teams":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/UsIqiH4.jpg',
                    preview_image_url='https://example.com/preview.jpg')) 
        if event.message.text == "Mc3 power gain teams":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/LBF0Rr9.jpg',
                    preview_image_url='https://example.com/preview.jpg'))   
        if event.message.text == "Mc3 unique teams":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/Zmec8Hs.jpg',
                    preview_image_url='https://example.com/preview.jpg'))
        
    return 'ok'
            
            
            
            
            
            
            
            
            
            
            
            
            
            
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
