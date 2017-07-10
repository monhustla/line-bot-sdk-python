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




app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('MyProject-3164a19e689c.json', scope)
gc = gspread.authorize(credentials)

line_bot_api = LineBotApi('EF7cmk1BxOG/UqSMMhiIMVw9Fy1EH4k3f+AGQnRSiaATp67WvyVwX62bpqGw6yPhOCznEfcePwycayIb6bQwCWQjvkR6ZuRnNl2WUFRzNALCfVkrY/+XwATYL3au1agq8C5KCY2b1lrCE5tZZh8ctAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1ba0ee354caf9e4f0e1b52c627b86ffc')


line_bot_api = LineBotApi('EF7cmk1BxOG/UqSMMhiIMVw9Fy1EH4k3f+AGQnRSiaATp67WvyVwX62bpqGw6yPhOCznEfcePwycayIb6bQwCWQjvkR6ZuRnNl2WUFRzNALCfVkrY/+XwATYL3au1agq8C5KCY2b1lrCE5tZZh8ctAdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('1ba0ee354caf9e4f0e1b52c627b86ffc')


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
    if champs is None:                                            # can't calculate a prestige from nothing, prevents a divide by 0 error
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
    print (top_champcount)
    top_champamount=sum(results)
    print (top_champamount)
    average=str(int(top_champamount/top_champcount))
    print (average)
    
    

    # And grab the average (as an integer since all inputs are integers
    # It has a precision of 1 so converting to int again will remove the trailing 0) e.g. 1234.0
    return (average)





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
                TextSendMessage(text="Hey, thank you for inviting the MCOC Concierge In-Chat Bot. All commands need to be prefaced with: Mc3."+'\n'+'\n'+
                                "Make sure you have auto-download images turned on in photos & videos settings!"+'\n'+'\n'+
                                "To learn how to setup the line prestige tool type: Mc3 prestige instructions."+"You can also join the bot support group here:"+'\n'+
                                "http://line.me/ti/g/r0yetwDGpc"
                                '\n'+'\n'+
                                "To get started type: Mc3 list"))
           
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        #if event.message.text=="Mc3 save profile":
            #json_line = request.get_json()
            #json_line = json.dumps(json_line)
           # decoded = json.loads(json_line)
            #user = decoded['events'][0]['source']['userId']
            #f=str(user)
            #profile= line_bot_api.get_profile(user)
            #name=(profile.display_name)
            #print(f)
            #cur=conn.cursor()
            #cur.execute("INSERT INTO prestige_data (lineid, summoner_name, champ_data) VALUES (%s, %s, %s);""",
           ##             (f, name, "whocares"))
           # cur.execute("SELECT lineid, summoner_name, champ_data FROM prestige_data  WHERE lineid= %(lineid)s""",
           #             {"lineid":f})
           # rows = cur.fetchall()
           # print(rows)
            #for row in rows:
                #print("    LINE ID: " + row[0] + "\n")
               # print("    Summoner: " + row[1] + "\n")
                #line_bot_api.reply_message(
                    #event.reply_token,
                    #TextSendMessage(text=(row[1]+": " + "added.")))
            
            
        eventText=event.message.text
        trigger = "Mc3 input champ:"
        if eventText.startswith(trigger):
            
            print(eventText)
            s = eventText[eventText.find(trigger) + len(trigger):]
            print(s) # 4-nebula-4 30
            pieces = s.split()                                    # ['4-nebula-4', '30']
            champ = pieces[0]
            sig = pieces[1]
            print (champ)
            print (sig)
            json_line = request.get_json()
            json_line = json.dumps(json_line)
            decoded = json.loads(json_line)
            user = decoded['events'][0]['source']['userId']
            print (user)
            f=str(user)
            profile= line_bot_api.get_profile(user)
            name=(profile.display_name)
            print (name)



            # We're going to bail out if the champion name isn't a valid one.
            # We should probably send back a message to the user too
            # We're returning the prestige now too so we don't have to hit the database twice!
            champ_prestige = get_prestige_for_champion(champ, sig)
            if champ_prestige is None:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Oops! You've entered an invalid champion or signature level."))
                continue                                          # this breaks out of our branch without exiting the bot script

            cur = None
            try:
                print (champ_prestige)
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                # get the user's information if it exists
                cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid = %(lineid)s""", {"lineid":f})
                rows = cur.fetchall()
                print (rows)

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
                    champ_data = json.loads('{}')                     # start with an empty list of champs
                    champs = {}                                    # creates an empty Python list
            except BaseException:
                if cur is not None:
                    cur.rollback()
                    cur.close()
                    continue
            finally:
                if cur is not None:
                    cur.close()

            # either way, let's move on

            # this will make sure that the Summoner's name is always updated if their Line profile has changed
            summoner_name = name

            # add or update the user's champ
            champs[champ] = champ_prestige

            # put everything together and send it back to the database
            champ_data = json.dumps(champs)


            # Checks for an existing line ID and updates if it exists or adds if it doesn't
            cur = None
            try:
                cur = conn.cursor()
                cur.execute("""INSERT INTO prestige_data(lineid, summoner_name, champ_data)
                               VALUES(%(lineid)s, %(summoner_name)s, %(champ_data)s)
                               ON CONFLICT (lineid)
                               DO UPDATE SET summoner_name = Excluded.summoner_name, champ_data = Excluded.champ_data;""",
                            {"lineid": lineid, "summoner_name": summoner_name, "champ_data": champ_data})
                conn.commit()
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=champ + " (" + champ_prestige + ") added"))
            except BaseException:
                if cur is not None:
                    conn.rollback()
            finally:
                if cur is not None:
                    cur.close()


        if event.message.text == "Mc3 my prestige":
            print ("nice")
            # Grab the user's champ data
            cur = None
            json_line = request.get_json()
            json_line = json.dumps(json_line)
            decoded = json.loads(json_line)
            user = decoded['events'][0]['source']['userId']
            try:
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                # get the user's information if it exists
                cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid = %(lineid)s LIMIT 1""", {"lineid": user})
                rows = cur.fetchall()
                print (rows)

                # The user exists in the database and a result was returned
                for row in rows:
                    msg =("Your prestige is: "+ calculate_prestige(row[2]))
                    break                                             # we should only have one result, but we'll stop just in case
                # The user does not exist in the database already
                else:
                    msg = "Oops! You need to add some champs first. Try 'mc3 input champ'."

                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=msg))
            except BaseException as e:
                print(e)
            finally:
                if cur is not None:
                    cur.close()

        if eventText == "Mc3 my champs":
            json_line = request.get_json()
            json_line = json.dumps(json_line)
            decoded = json.loads(json_line)
            user = decoded['events'][0]['source']['userId']
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid = %(lineid)s""", {'lineid': user})
            rows = cur.fetchall()
            for row in rows:
                champs=row[2]
                if champs is None:
                    msg = "Oops! You need to add some champs first. Try 'mc3 input champ'."
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=msg))
            if conn is None:
                cur.close()
              
            else:
                for row in rows:
                    champs = row[2]
                    champs = json.loads(champs)
                    top_champs = sorted(champs, reverse=True)[:5]
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=str(champs)))
                        
        if event.message.text == "Mc3 clear champs":
            json_line = request.get_json()
            json_line = json.dumps(json_line)
            decoded = json.loads(json_line)
            user = decoded['events'][0]['source']['userId']
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)                      
            cur.execute("""DELETE FROM prestige_data WHERE lineid = %(lineid)s""", {'lineid': user})
            conn.commit()
            rows=cur.fetchall()
            print (rows)
            if cur is not None:
                conn.rollback()
            if cur is not None:
                conn.close()
               
        if "Mc3 remove:" in event.message.text:
            json_line = request.get_json()
            json_line = json.dumps(json_line)
            decoded = json.loads(json_line)
            user = decoded['events'][0]['source']['userId']
            s1=event.message.text
            s2=":"
            champ=(s1[s1.index(s2)+len(s2):])
            cur=None
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)            
            cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid = %(lineid)s""", {"lineid":user})
            rows = cur.fetchall()
            for row in rows:
                champs = json.loads(row['champ_data'])   
                champs.pop(champ, None)
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=champ+'\n'+" has been removed."))
                conn.commit()
                if cur is not None:
                    conn.rollback()
                if cur is not None:
                    conn.close()
                
                
                
                   
        if event.message.text == "Mc3 og vision lol":
            line_bot_api.reply_message(
                event.reply_token,
                VideoSendMessage(
                    original_content_url='https://dl.dropboxusercontent.com/s/hiak83i7qzr7p5a/og%20vision.mp4',
                    preview_image_url='https://dl.dropboxusercontent.com/s/hiak83i7qzr7p5a/og%20vision.mp4'))
        if "Mc3 abilities:" in event.message.text:
            s1=event.message.text
            s2=":"
            name=(s1[s1.index(s2)+len(s2):])
            wb = load_workbook('champbios.xlsx')
            ws=wb[name]
            signature=ws.cell(column=2,row=4).value
            passive=ws.cell(column=2,row=8).value
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Signature Ability: "+'\n'+signature+'\n'+'\n'+
                               "Passive Ability: "+'\n'+passive))            
                        
        #Whole List Breakdown    
        if event.message.text == "Mc3 list":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Make sure you have auto-download images turned on in photos & videos settings!"+'\n'+'\n'+
                                "Command List:"+'\n'+
                                "abilities"+'\n'+
                                "aq"+'\n'+"aw"+'\n'+"arena"+'\n'+"calendars"+'\n'+"duels"+'\n'+"masteries"+'\n'+"prestige"+'\n'+"special quests"+'\n'+"synergies"))     
        
        if event.message.text == "Mc3 abilities":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="To use Mc3 abilities, you must type: Mc3 abilities:(champname). An example would be: Mc3 abilities:spidergwen"))
            
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
                    preview_image_url='https://i.imgur.com/BvLSyYt.jpg'))
                    
        if event.message.text == "Mc3 aq rewards":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/ZwdRIoj.jpg',
                    preview_image_url='https://i.imgur.com/ZwdRIoj.jpg'
                )
            )
            
        if event.message.text == "Mc3 boss practice":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/71x09Rm.jpg',
                    preview_image_url='https://i.imgur.com/71x09Rm.jpg'
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
                    original_content_url='https://i.imgur.com/GZYgvhS.jpg',  #updated
                    preview_image_url='https://i.imgur.com/fSejvcF.jpg'))
            
        if event.message.text == "Mc3 map 4":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Coming soon")) 
            
        if event.message.text == "Mc3 map 5":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/TqTHnKB.jpg',  #updated
                    preview_image_url='https://i.imgur.com/IddfRDM.jpg'))
            
        if event.message.text == "Mc3 map 6":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/Eie596I.jpg',  #updated
                    preview_image_url='https://i.imgur.com/8cOa78V.jpg'))
            
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
                    preview_image_url='https://i.imgur.com/ZxgWTY7.jpg'))
        
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
                    preview_image_url='https://i.imgur.com/LWHaCCv.jpg'))
        if event.message.text == "Mc3 t4b":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/EwC1hdp.jpg',
                    preview_image_url='https://i.imgur.com/EwC1hdp.jpg'))
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
                    preview_image_url='https://i.imgur.com/iyNbSOk.jpg'))            
        if event.message.text == "Mc3 monthly calendar":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/WAWxx7k.jpg',
                    preview_image_url='https://i.imgur.com/WAWxx7k.jpg'))  
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
                    preview_image_url='https://i.imgur.com/Mc3aao5.jpg'))           
        if event.message.text == "Mc3 mastery builder":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="https://alsciende.github.io/masteries/v10.0.1/#0000000000000000000000000000000000000010000000000000000"))            
        if event.message.text == "Mc3 mastery pi":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/T12L38x.jpg',
                    preview_image_url='https://i.imgur.com/T12L38x.jpg'))          
            
            
        #Prestige Command Tree
        if event.message.text == "Mc3 prestige":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="prestige calculator"+'\n'+"prestige list"+'\n'+"prestige tools"))         
            #Prestige Keywords
        if event.message.text == "Mc3 prestige calculator":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="https://docs.google.com/spreadsheets/d/1YdOWdX2zpyWBBLos36CthqpJ9y1HlPdSHV8jtvkeF3E/copy"))
        if event.message.text == "Mc3 prestige list":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="https://docs.google.com/spreadsheets/d/1Cd3-X2lAQyJBlBuxBld6fsWBw4HkBdm2AFybHk3nfS4/pubhtml#"))
        if event.message.text == "Mc3 prestige tools":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="You must first add the bot to use the prestige tools. Also, becareful of spaces and syntax."+'\n'+'\n'+
                                "The following commands are verbatim, simply remove the parenthesis and plug in the code within the parenthesis:"+'\n'+
                                "(Mc3 prestige instructions)- Instructions on how to get setup."+'\n'+
                                "(Mc3 input champ:5-gwenpool-4 99)-That's a 5* rank 4 gwenpool sig level 99"+'\n'+
                                "(Mc3 my champs)"+'\n'+
                                "(Mc3 my prestige)"+'\n'+
                                "(Mc3 clear champs) clears all of your saved champs"))
        if event.message.text == "Mc3 prestige instructions":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="This won't work if you haven't set a line id yet. That's how everything is stored. If you don't have one, set it and restart your device. Everyone who has a line id, just add the bot and input a champ to store yourself. You will be free to use the bot anywhere after a champ has been added. For a picture example of getting set-yp type: Mc3 prestige example"))
        if event.message.text == "Mc3 prestige example":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/9IHlaLj.jpg',
                    preview_image_url='https://i.imgur.com/9IHlaLj.jpg'))       
                        
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
                    preview_image_url='https://i.imgur.com/vB3Ix7L.jpg'))
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
                    preview_image_url='https://i.imgur.com/WTyyl7t.jpg'))
        if event.message.text == "Mc3 bleed teams":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Coming Soon"))
        if event.message.text == "Mc3 crit teams":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/UsIqiH4.jpg',
                    preview_image_url='https://i.imgur.com/UsIqiH4.jpg')) 
        if event.message.text == "Mc3 power gain teams":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/LBF0Rr9.jpg',
                    preview_image_url='https://i.imgur.com/LBF0Rr9.jpg'))   
        if event.message.text == "Mc3 unique teams":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/Zmec8Hs.jpg',
                    preview_image_url='https://i.imgur.com/Zmec8Hs.jpg'))
        

        return 'ok'
            
            
            
            
            
            
            
            
            
            
            
            
            
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
