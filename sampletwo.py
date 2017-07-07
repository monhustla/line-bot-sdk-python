from __future__ import unicode_literals
import os
from os import environ
import sys
import tempfile
import psycopg2
import psycopg2.extras
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

def get_prestige_for_champion(champ, sig):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT prestige FROM prestige_table WHERE champ = '%(champ)s' AND sig = '%(sig)i'""", {champ, sig})
    rows = cur.fetchall()
    for row in rows:
        return str(row['prestige'])                               # Returns a prestige value
    else:
        return None                                               # Returns None if a champ or sig wasn't found

def calculate_prestige(champs):
    if champs is None:                                            # can't calculate a prestige from nothing, prevents a divide by 0 error
        return 0

    # if champs isn't a dict, it might still be a JSON string
    if not type(champs) is dict:
        champs = json.loads(champs)

    # Ok, here's a little one-liner wonder:
    #    First, we sort the array in descending order
    #    Then, we slice off the first 5 elements (if there are that many)
    top_champs = sorted(champs.values(), reverse=True)[:5]

    # And grab the average (as an integer since all inputs are integers
    # It has a precision of 1 so converting to int again will remove the trailing 0) e.g. 1234.0
    return int(sum(top_champs) / len(top_champs))





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
        trigger = "mc3 input champ"
        eventText=event.message.text
        if eventText.lower().startswith(trigger):                 # mc3 input champ 4-nebula-4 30
            s = eventText[eventText.lower().find(trigger) + len(trigger):]   # 4-nebula-4 30
            pieces = s.split()                                    # ['4-nebula-4', '30']
            champ = pieces[0]
            print (champ)
            sig = pieces[1]
            print (sig)

            # We're going to bail out if the champion name isn't a valid one.
            # We should probably send back a message to the user too
            # We're returning the prestige now too so we don't have to hit the database twice!
            champ_prestige = get_prestige_for_champion(champ, sig)
            if champ_prestige is None:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Oops! You've entered an invalid champion or signature level."))
                continue                                          # this breaks out of our branch without exiting the bot script


            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # get the user's information if it exists
            cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid = '%(lineid)s'""", {"lineid": user})
            rows = cur.fetchall()

            # The user exists in the database and a result was returned
            for row in rows:
                lineid = row['lineid']
                summoner_name = row['summoner_name']
                champs = json.loads(row['champ_data'])            # contains a list of the user's champs
                break                                             # we should only have one result, but we'll stop just in case
            # The user does not exist in the database already
            else:
                lineid = user
                summoner_name = name
                #champ_data = json.loads('{}')                     # start with an empty list of champs
                champs = {}                                    # creates an empty Python list
            
            # either way, let's move on

            # this will make sure that the Summoner's name is always updated if their Line profile has changed
            summoner_name = name

            # add or update the user's champ
            champs[champ] = champ_prestige

            # put everything together and send it back to the database
            champ_data = json.whatever(champs)


            # Checks for an existing line ID and updates if it exists or adds if it doesn't
            cur = conn.cursor()
            cur.execute("""INSERT INTO prestige_data(lineid, summoner_name, champ_data),
                           VALUES('%(lineid)s', '%(summoner_name)s', '%(champ_data)s')
                           ON CONFLICT (lineid)
                           DO UPDATE SET summoner_name = Excluded.summoner_name, champ_data = Excluded.champ_data;""",
                        {lineid, summoner_name, champ_data})

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=champ + " (" + champ_prestige + ") added"))

        trigger = "mc3 get prestige"
        if eventText.lower().startswith(trigger):
            # Grab the user's champ data
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # get the user's information if it exists
            cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid = '%(lineid)s' LIMIT 1""", {"lineid": user})
            rows = cur.fetchall

            # The user exists in the database and a result was returned
            for row in rows:
                msg = get_prestige_for_champion(row['champ_data'])
                break                                             # we should only have one result, but we'll stop just in case
            # The user does not exist in the database already
            else:
                msg = "Oops! You need to add some champs first. Try 'mc3 input champ'."

            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
                
                   
                        
                        
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
