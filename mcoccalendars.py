# -*- coding: utf-8 -*-

"""calendar module."""

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

class calendar(cmd2.Cmd):

    def __init__(self, line_bot_api, event):
        self.line_bot_api = line_bot_api
        self.event = event
        super(calendar, self).__init__()
        
    def default(self, line):
        #self.line_bot_api.reply_message(self.event.reply_token,
        #    TextSendMessage(text="Oops! You've entered an invalid aq command please type " + 
        #    self.trigger + "calendar to view available commands"))
        return False

    def do_daily(self,line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/iyNbSOk.jpg',
                    preview_image_url='https://i.imgur.com/iyNbSOk.jpg'))
        return True
        
    def do_monthly(self,line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/WAWxx7k.jpg',
                    preview_image_url='https://i.imgur.com/WAWxx7k.jpg'))
        return True

    def do_premium(self,line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text="http://marveltrucos.x10.mx/premium.php"))
        return True

    def do_basic(self,line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text="http://marveltrucos.x10.mx/basics.php"))
        return True
        
    def do_new5stars(self,line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/4SW1fF3.jpg',
                    preview_image_url='https://i.imgur.com/4SW1fF3.jpg')) 
        return True        

    def do_EOF(self, line):
        return True

    def process(self, line):
        return self.onecmd(line);
