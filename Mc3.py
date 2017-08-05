# -*- coding: utf-8 -*-

"""Mc3 module."""

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

#from aq import (aq, map, boss)
#from arena import arena
#from aw import aw
#from mcoccalendars import calendar
#from prestigetest import inputchamp
from cutoffs import cutoffs


class Mc3(cmd2.Cmd):
    trigger = 'Mc3 '

    def __init__(self, line_bot_api, event):
        self.line_bot_api = line_bot_api
        self.event = event
        super(Mc3, self).__init__()
        
    #def default(self, line):
         #self.line_bot_api.reply_message(self.event.reply_token,
         #   TextSendMessage(text="Oops! You've entered an invalid command please type " + 
         #   self.trigger + "list to view available commands"))
    #    return False
    
    
    def do_cutoffs(self, line):
        _cutoffs = cutoffs(self.line_bot_api, self.event)
        
        return _cutoffs.cutoffs(line)     
                               



        
    def do_EOF(self, line):
        return True

    def process(self, line):
        return self.onecmd(line);
