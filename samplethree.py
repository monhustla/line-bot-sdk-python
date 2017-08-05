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


db_url = os.environ.get('DATABASE_URL', None)
if db_url:
    url = urlparse.urlparse(db_url)
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
    #conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)




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
    print(top_champs)
    results = list(map(int, top_champs)) 
    print(results)
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
    alliancep=(int(top_playeramount/top_playercount)) 

    # And grab the average (as an integer since all inputs are integers
    # It has a precision of 1 so converting to int again will remove the trailing 0) e.g. 1234.0
    return (str(alliancep))


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
        if isinstance(event, JoinEvent):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Hey, thank you for inviting the MCOC Concierge In-Chat Bot. All commands need to be prefaced with: 'Mc3'."+'\n'+'\n'+
                                "Example:'Mc3 arena'"+'\n'+"Make sure every letter is lower case after the M in Mc3, and also make sure to now have spaces after the last letter in the command."+'\n'+'\n'+
                                "To learn how to setup the line prestige tool type: Mc3 prestige instructions."+"You can also join the bot support group here:"+'\n'+
                                "http://line.me/ti/g/r0yetwDGpc"
                                '\n'+'\n'+
                                "To get started type: 'Mc3 list'"))
           
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
                
        
        if eventTextLower=="mc3 my champs":
            print("My champs:"+eventText)
            user=event.source.user_id
            print(user)
            if user is None:
                msg = "You need to add some champs first. Click on my picture and start a chat with me to get started, or type'Mc3 prestige instructions'."
                print("user is none: ")
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=msg))
                return
                
                
            else:    
                cur=None
                
            #profile= line_bot_api.get_profile(user)
            #name=str((profile.display_name))
            #name = ""

           
                try:
                    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                    # get the user's information if it exists
                    cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid = %(lineid)s LIMIT 1""", {"lineid": user})
                    rows = cur.fetchall()
                    
                    print (rows)
                    #if cur is None:
                    for row in rows:                        
                        name=row[1]
                        champs = row[2]
                        print (champs)
                        
                        prestige=(calculate_prestige(champs))
                        print(prestige)
                        champs = json.loads(champs)                       
                        champsdict=dict.items(champs)
                        champs_sorted=sorted(champsdict, key=lambda student: student[1], reverse=True)
                        l=('\n'.join(map(str,champs_sorted)))
                        hello=str(l).replace('(', '').replace(')', '')
                        yay=str(hello).replace("'", "").replace("'", "")
                        msg=(yay+'\n'+"---------------------------"+'\n'+name+'\n'+"Prestige:"+(str(prestige)))
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=msg))
                        print("Successful my champs")
                        conn.commit()
                        cur.close()
                        break
                    else:
                        msg = "You need to add some champs first. Click on my picture and start a chat with me to get started, or type'Mc3 prestige instructions'."
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=msg))
                        return
                        print("person had no champs")
                        conn.commit()
                        cur.close()
                        return


                except BaseException as e:
                    if cur is not None:
                        conn.rollback()
                        cur.close()
                        print("rollback")
                        print("Their id isn't set messed up with my champs")
                        msg = "You need to add some champs first. Click on my picture and start a chat with me to get started, or type'Mc3 prestige instructions'."
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=msg))
                        return
                        
                finally:
                    if cur is not None:
                        print("My champs committed: see if it was successful or not")
                        conn.commit()
                        cur.close()
                        
                                              
        if eventTextLower=="mc3 my prestige":
            print("Working on prestige"+eventTextLower)
        
            user=event.source.user_id
            print("My champs:"+eventText)
            user=event.source.user_id
            if user is None:
                msg = "You need to add some champs first. Click on my picture and start a chat with me to get started, or type'Mc3 prestige instructions'."
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=msg))
                
                
            else:

            # Grab the user's champ data
                cur = None
                try:
                    #profile= line_bot_api.get_profile(user)
                    #name=str((profile.display_name))
                    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

                    # get the user's information if it exists
                    cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid = %(lineid)s LIMIT 1""", {"lineid": user})
                    rows = cur.fetchall()


                    # The user exists in the database and a result was returned
                    for row in rows:
                        msg =("Your prestige is: "+ calculate_prestige(row[2]))
                        print("We have calculated the prestige")
                        break                                             # we should only have one result, but we'll stop just in case
                    # The user does not exist in the database already
                    else:
                        msg = "You need to add some champs first. Click on my picture and start a chat with me to get started, or type'Mc3 prestige instructions'."

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=msg))


                except (BaseException) as e:
                    print("error")
                    if cur is not None:
                        conn.rollback()
                        print("my prestige fail")
                        cur.close()
                finally:
                    if cur is not None:
                        print("my prestige success")
                        conn.commit()
                        cur.close()                                                              

        if eventTextLower == "mc3 clear champs":
            try:
                cur=None
                user=event.source.user_id
                print(user)
               
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)                      
                cur.execute("""DELETE FROM prestige_data WHERE lineid = %(lineid)s""", {'lineid': user})
                conn.commit()
                print("successful")
                if cur is not None:
                    conn.rollback()
                if cur is not None:
                    cur.close()
                    cur=None
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
                cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid = %(lineid)s""", {'lineid': user})
                rows = cur.fetchall()
                #cur.commit()
                print (rows)
                if rows ==[]:
                    print("hey")
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="Your champs have been removed."))
                        
            except BaseException:
                if cur is not None:
                    print("base exception")
                    conn.rollback()
                    cur.close()
            finally:
                if cur is not None:
                    print("done")
                    conn.commit()
                    cur.close()
                
        trigger="mc3 remove "
        if trigger in eventTextLower:
            print(eventText)
            user=event.source.user_id
            #profile= line_bot_api.get_profile(user)
            #name=str((profile.display_name))
            name = ""
            try:
                s = eventText[eventText.find(trigger) + len(trigger):]
                pieces = s.split()                                    
                champ = pieces[0]
                cur=None
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)            
                cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid = %(lineid)s""", {"lineid":user})
                rows = cur.fetchall()
                for row in rows:
                    name = row['summoner_name']
                    champs = json.loads(row['champ_data'])
                    champs.pop(champ, None)
                    champ_data = json.dumps(champs)
                    
            except BaseException:
                if cur is not None:
                    conn.rollback()
                    return
            finally:
                if cur is not None:
                    cur.close()        
            
            cur=None
            try:
                cur = conn.cursor()
                cur.execute("""INSERT INTO prestige_data(lineid, summoner_name, champ_data)
                           VALUES(%(lineid)s, %(summoner_name)s, %(champ_data)s)
                           ON CONFLICT (lineid)
                           DO UPDATE SET summoner_name = Excluded.summoner_name, champ_data = Excluded.champ_data;""",
                        {"lineid": user, "summoner_name": name, "champ_data": champ_data})
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=champ+'\n'+" has been removed."))
                
                conn.commit()
                print("successful remove")
            except BaseException:
                if cur is not None:
                    conn.rollback()
                    cur.close()
                    return
            finally:
                if cur is not None:
 
                    cur.close()
                    

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
          
        
        
        
            
        if eventTextLower == "mc3 champ list":
            if event.source.type=='user':
                
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="abomination"+'\n'+"agentvenom"+'\n'+"angela"+'\n'+"antman"+'\n'+"archangel"+'\n'+"beast"+'\n'+"blackbolt"+'\n'+"blackpanther"+'\n'+"blackpanthercw"+'\n'+"blackwidow"+'\n'+"cable"+'\n'+
                                    "captainamerica"+'\n'+"captainamericawwii"+'\n'+"captainmarvel"+'\n'+"carnage"+'\n'+"civilwarrior"+'\n'+"colossus"+'\n'+"crossbones"+'\n'+"cyclops"+'\n'+"cyclops90s"+'\n'+"daredevil"+'\n'+
                                    "daredevilnetflix"+'\n'+"deadpool"+'\n'+"deadpoolxforce"+'\n'+"dormammu"+'\n'+"drax"+'\n'+"drstrange"+'\n'+"drvoodoo"+'\n'+"electro"+'\n'+"elektra"+'\n'+"falcon"+'\n'+"gambit"+'\n'+"gamora"+'\n'+
                                    "ghostrider"+'\n'+"groot"+'\n'+"guillotine"+'\n'+"gwenpool"+'\n'+"hawkeye"+'\n'+"hood"+'\n'+"howard"+'\n'+"hulk"+'\n'+"hulkbuster"+'\n'+"hyperion"+'\n'+"iceman"+'\n'+"ironfist"+'\n'+
                                    "ironfistwhite"+'\n'+"ironman"+'\n'+"ironpatriot"+'\n'+"joefixit"+'\n'+"juggernaut"+'\n'+"kamalakhan"+'\n'+"kang"+'\n'+"karnak"+'\n'+"kinggroot"+'\n'+"loki"+'\n'+"lukecage"+'\n'+"magik"+'\n'+"magneto"+'\n'+
                                    "magnetomarvelnow"+'\n'+"moonknight"+'\n'+"mordo"+'\n'+"msmarvel"+'\n'+"nebula"+'\n'+"nightcrawler"+'\n'+"phoenix"+'\n'+"psylocke"+'\n'+"punisher"+'\n'+"quake"+'\n'+"redhulk"+'\n'+
                                    "rhino"+'\n'+"rocket"+'\n'+"rogue"+'\n'+"ronan"+'\n'+"scarletwitch"+'\n'+"shehulk"+'\n'+"spidergwen"+'\n'+
                                    "spiderman"+'\n'+"spidermanblack"+'\n'+"spidermanmorales"+'\n'+"starlord"+'\n'+"storm"+'\n'+"superiorironman"+'\n'+"thanos"+'\n'+"thevision"+'\n'+"thor"+'\n'+"thorjanefoster"+'\n'+
                                    "ultron"+'\n'+"ultron_classic"+'\n'+"unstoppablecolossus"+'\n'+"venom"+'\n'+"venompool"+'\n'+"vision"+'\n'+"warmachine"+'\n'+"wintersoldier"+'\n'+"wolverine"+'\n'+"wolverineoldman"+'\n'+
                                    "x23"+'\n'+"yellowjacket"+'\n'+"yondu"))

            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="This command only works in pm with me."))
                
        if eventTextLower=="mc3 line prestige":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="'Mc3 prestige instructions'"+'\n'+"'Mc3 inputchamp' Example-'Mc3 inputchamp 5-drvoodoo-4 99'"+'\n'+"'Mc3 my champs'"+'\n'+"'Mc3 my prestige'"+'\n'+"'Mc3 remove ' Example-'Mc3 remove 5-drvoodoo-4'"+'\n'+"'Mc3 clear champs'-This removes all saved champs"+'\n'+
                                "'Mc3 lookup (champname)'- Gets you the prestige of one champ without adding them"+'\n'+"'Mc3 test (champname)'- Gets your prestige if you were to add the champ"+'\n'+
                               "'Mc3 champ list' -A list of the syntax for every champ name in the calculator"))
        
       
        
        #if eventTextLower=="mc3 alliance prestige":
        #    line_bot_api.reply_message(
        #        event.reply_token,
        #        TextSendMessage(text="'Mc3 alliance prestige instructions'"+'\n'+"'Mc3 add alliance:(alliance tag) password:(alliance password)'"+'\n'+"'Mc3 join:(alliance tag) password:(alliance password)'"+'\n'+"'Mc3 alliance:(alliance tag) password:(alliance password)'"+'\n'+
        #                       "'Mc3 leave:(alliance tag)'"))
            
        if eventTextLower == "mc3 alliance prestige instructions":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Steps"+'\n'+"1.)Add your alliance. To do so you use the 'Mc3 add alliance:(alliange tag) password(alliance password)' command and also set-up an alliance password."+'\n'+"Example-"+'\n'+
                               "'Mc3 add alliance:H4M2N password:FH3'"+'\n'+"The alliance tag was 'H4M2N' and the alliance password was 'FH3'. Every alliance command will utilize this password so save it in your alliance chat notes."+'\n'+'\n'+
                               "2.)You are already a member of the alliance you created. Now for other members to join, they must type in the command 'Mc3 join:(alliance tag) password:(alliance password)'"+'\n'+"Example:"+'\n'+
                               "Mc3 join:H4M2N password:FH3'"+'\n'+"This new member is now joined to your alliance."+'\n'+'\n'+
                               "3.)The tool automatically calculates your alliance prestige. To see your members and prestige use the command 'Mc3 alliance:(alliance tag) password:(alliance password)'"+'\n'+
                               "Example:"+'\n'+ "'Mc3 alliance:H4M2N password:FH3'"+'\n'+'\n'+
                               "4.)To leave an alliance use the command 'Mc3 leave:(alliance tag)'"+'\n'+"Example:"+'\n'+
                               "'Mc3 leave:H4M2N' Note, you do not need a password for this command."))   
            
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
    
