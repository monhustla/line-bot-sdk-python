# -*- coding: utf-8 -*-

"""cutoffs module."""

import cmd2
import json
import re



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

data_file=open('cutoffs.json')
cutoffs1=json.load(data_file)



class cutoffs(cmd2.Cmd):

    def __init__(self, line_bot_api, event):
        self.line_bot_api = line_bot_api
        self.event = event
        super(cutoffs, self).__init__()
        
    def default(self, line):
        self.line_bot_api.reply_message(self.event.reply_token,
            TextSendMessage(text="To access cutoff for a particular champ try 'Mc3 cutoffs (champ)'."+'\n'+
                            "Example: Mc3 cutoffs spidermanstark"))
        return False    

    def cutoffs(self,line):
                                         # ['4-nebula-4', '30']
        champ = line
        print(champ)
        if not champ or champ == '':
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text='Please enter a champ name for cuttoffs'))
            return True
        
        try:
            scores=cutoffs1.get(champ, None)
            if not scores:
                self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text='No cuttoffs found for champ: ' + champ))
                return True;

            round2=str(scores[0].values()).replace("dict_values",'').replace("(",'').replace("[",'').replace("'",'').replace("]",'').replace(")",'')
            print(round2)
            round1=str(scores[1].values()).replace("dict_values",'').replace("(",'').replace("[",'').replace("'",'').replace("]",'').replace(")",'')
            print(round1)
            h=("Round 1: "+round1+'\n'+"Round 2: "+round2)
            print(h)
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text=h))
          
        except:
            print("there is nothing here")
            self.line_bot_api.reply_message(
                    self.event.reply_token,
                    TextSendMessage(text="Incorrect input or cutoff data not available."))
