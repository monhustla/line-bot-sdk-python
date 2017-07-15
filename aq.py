# -*- coding: utf-8 -*-

"""aq module."""

import cmd2

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

class aq(cmd2.Cmd):

    def __init__(self, line_bot_api, event):
        self.line_bot_api = line_bot_api
        self.event = event
        super(aq, self).__init__()
        
    def default(self, line):
        #self.line_bot_api.reply_message(self.event.reply_token,
        #    TextSendMessage(text="Oops! You've entered an invalid aq command please type " + 
        #    self.trigger + "aq to view available commands"))
        return False
    
    def do_cost(self,line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/BvLSyYt.jpg',
                    preview_image_url='https://i.imgur.com/BvLSyYt.jpg'))
        return True

    def do_rewards(self,line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/ZwdRIoj.jpg',
                    preview_image_url='https://i.imgur.com/ZwdRIoj.jpg'))

        return True 
    
    def do_maps(self,line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text="interactive maps"+'\n'+"map 3"+'\n'+"map 4"+'\n'+"map 5"+'\n'+"map 6"))  

        return True     
    

    def do_EOF(self, line):
        return True

    def process(self, line):
        return self.onecmd(line);

class map(cmd2.Cmd):
    
    def __init__(self, line_bot_api, event):
        self.line_bot_api = line_bot_api
        self.event = event
        super(map, self).__init__()
        
    def default(self, line):
        #self.line_bot_api.reply_message(self.event.reply_token,
        #    TextSendMessage(text="Oops! You've entered an invalid aq command please type " + 
        #    self.trigger + "aq to view available commands"))
        return False

    def do_3(self,line):
        self.line_bot_api.reply_message(
        self.event.reply_token,
        ImageSendMessage(
            original_content_url='https://i.imgur.com/GZYgvhS.jpg',  
            preview_image_url='https://i.imgur.com/fSejvcF.jpg'))
        return True    

    def do_5(self,line):
        self.line_bot_api.reply_message(
            self.event.reply_token,
            ImageSendMessage(
                original_content_url='https://i.imgur.com/BvLSyYt.jpg',
                preview_image_url='https://i.imgur.com/BvLSyYt.jpg'))
        return True 

    def do_6(self,line):
        self.line_bot_api.reply_message(
            self.event.reply_token,
            ImageSendMessage(
                original_content_url='https://i.imgur.com/Eie596I.jpg',  
                preview_image_url='https://i.imgur.com/8cOa78V.jpg'))
        return True

    def do_EOF(self, line):
        return True

    def process(self, line):
        return self.onecmd(line);
    
class boss(cmd2.Cmd):
    def __init__(self, line_bot_api, event):
            self.line_bot_api = line_bot_api
            self.event = event
            super(boss, self).__init__()
        
    def default(self, line):
        #self.line_bot_api.reply_message(self.event.reply_token,
        #    TextSendMessage(text="Oops! You've entered an invalid aq command please type " + 
        #    self.trigger + "aq to view available commands"))
        return False

    def do_practice(self,line):
        self.line_bot_api.reply_message(
        self.event.reply_token,
        ImageSendMessage(
            original_content_url='https://i.imgur.com/71x09Rm.jpg',
            preview_image_url='https://i.imgur.com/71x09Rm.jpg'))
        return True 

    def do_EOF(self, line):
        return True

    def process(self, line):
        return self.onecmd(line);
