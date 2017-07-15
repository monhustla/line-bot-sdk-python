# -*- coding: utf-8 -*-

"""aw module."""

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

class aw(cmd2.Cmd):

    def __init__(self, line_bot_api, event):
        self.line_bot_api = line_bot_api
        self.event = event
        super(aw, self).__init__()
        
    def default(self, line):
        self.line_bot_api.reply_message(self.event.reply_token,
            TextSendMessage(text="Oops! You've entered an invalid aq command please type " + 
            self.trigger + "aw to view available commands"))
        return False
    
    def do_map(self,line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/ZxgWTY7.jpg',
                    preview_image_url='https://i.imgur.com/ZxgWTY7.jpg'))
        return True

        
    def do_EOF(self, line):
        return True

    def process(self, line):
        return self.onecmd(line);
