# -*- coding: utf-8 -*-

"""arena module."""

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

class arena(cmd2.Cmd):

    def __init__(self, line_bot_api, event):
        self.line_bot_api = line_bot_api
        self.event = event
        super(arena, self).__init__()
        
    def default(self, line):
        #self.line_bot_api.reply_message(self.event.reply_token,
        #    TextSendMessage(text="Oops! You've entered an invalid aq command please type " + 
        #    self.trigger + "arena to view available commands"))
        return False
    
    def do_basic(self,line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/LWHaCCv.jpg',
                    preview_image_url='https://i.imgur.com/LWHaCCv.jpg'))
        return True

    def do_t4b(self,line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/EwC1hdp.jpg',
                    preview_image_url='https://i.imgur.com/EwC1hdp.jpg'))

        return True 

    def do_cutoffs(self,line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text="https://docs.google.com/spreadsheets/d/1sJtSVnjhhRNxpiuMR5uXrsTlrsXMjp9TNO7JHDXhtsk/htmlview"))

        return True
        
    def do_EOF(self, line):
        return True

    def process(self, line):
        return self.onecmd(line); 
