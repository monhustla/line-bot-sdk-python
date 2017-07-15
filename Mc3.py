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

from aq import (aq, map, boss)
from arena import arena
from aw import aw
from mcoccalendars import calendar
#from prestigetest import inputchamp


class Mc3(cmd2.Cmd):
    trigger = 'Mc3 '

    def __init__(self, line_bot_api, event):
        self.line_bot_api = line_bot_api
        self.event = event
        super(Mc3, self).__init__()
        
    def default(self, line):
         #self.line_bot_api.reply_message(self.event.reply_token,
         #   TextSendMessage(text="Oops! You've entered an invalid command please type " + 
         #   self.trigger + "list to view available commands"))
        return False
    
    def do_list(self, line):
        self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text="Make sure all commands start with the 'Mc3' trigger and there are no spaces after the last letter in the command!"+'\n'+
                                     "Example:'Mc3 aq'"+'\n'+
                                     '\n'+
                                     "Command List:"+'\n'+
                                     "abilities"+'\n'+
                                     "aq"+'\n'+
                                     "aw"+'\n'+
                                     "arena"+'\n'+
                                     "calendars"+'\n'+
                                     "duels"+'\n'+
                                     "masteries"+'\n'+
                                     "prestige"+'\n'+
                                     "prestige tools"+'\n'+
                                     "special quests"+'\n'+
                                     "synergies"+'\n'+
                                     "support"+'\n'+
                                     "Inputting champs has changed, please see new syntax in 'Mc3 prestige tools'"))   
                               
        return True;

    def do_aq(self, line):
        _aq = aq(self.line_bot_api, self.event)
        
        return _aq.process(line.parsed.args)
    
    def do_map(self, line):
        _map = map(self.line_bot_api, self.event)
        
        return _map.process(line.parsed.args)
    
    def do_boss(self, line):
        _boss = boss(self.line_bot_api, self.event)
        
        return _boss.process(line.parsed.args)

    def do_arena(self, line):
        _arena = arena(self.line_bot_api, self.event)
        
        return _arena.process(line.parsed.args)
    
    def do_aw(self, line):
        _aw = aw(self.line_bot_api, self.event)
        
        return _aw.process(line.parsed.args)
    
    def do_calendar(self, line):
        _calendar = calendar(self.line_bot_api, self.event)
        
        return _calendar.process(line.parsed.args)
    
    #def do_inputchamp(self, line):
       # _inputchamp=inputchamp(self.line_bot_api, self.event,self.events, self.user)
        
        
        #return _inputchamp.splitname(line)

    def do_help(self, line):
        return self.do_list(line);
        
    def do_EOF(self, line):
        return True

    def process(self, line):
        return self.onecmd(line);
