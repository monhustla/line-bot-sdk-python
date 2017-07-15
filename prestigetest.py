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
import cmd2

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

class inputchamp(cmd2.Cmd):
    
    def __init__(self, line_bot_api,event,events,user):
        self.line_bot_api = line_bot_api
        self.event = event
        self.events=events
        self.user=user
        
        super(inputchamp, self).__init__()

     
            

       
    def splitname(self,line):
        line_bot_api=self.line_bot_api
        event=self.event
        events=self.events
        user=self.user
        print(user)  
        eventText=event.message.text
        trigger="Mc3 inputchamp "
        s = eventText[eventText.find(trigger) + len(trigger):]
         # 4-nebula-4 30
        pieces = s.split()                                    # ['4-nebula-4', '30']
        champ = pieces[0]
        sig = pieces[1]
        profile= line_bot_api.get_profile(user)
        name=(profile.display_name)
        print(name)
        print (champ)
        print (sig)
        champ_prestige = get_prestige_for_champion(champ, sig)
        if champ_prestige is None:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Oops! You've entered an invalid champion or signature level."))
                                                     # this breaks out of our branch without exiting the bot script

        cur = None
        try:
            print (champ_prestige)
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # get the user's information if it exists
            cur.execute("""SELECT lineid, summoner_name, champ_data FROM prestige_data WHERE lineid = %(lineid)s""", {"lineid":user})
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
        except psycopg2.Error:
            conn.rollback()
            print("PostgreSQL Error: " + e.diag.message_primary)
            pass
        finally:
            if cur is not None:
                cur.close()

    def do_EOF(self, line):
            return True

    def process(self, line):
        return self.onecmd(line);
