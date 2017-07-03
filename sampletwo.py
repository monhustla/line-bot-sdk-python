import os
from os import environ
import sys
import tempfile

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
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent, ImageSendMessage
)




app = Flask(__name__)



line_bot_api = LineBotApi('jCCJTBH9PKP0UzrCtVCpT99E2kOPn3bowhUA8KX1hcxMHwqdZbfLzP/I6leONvKqZmNyqKC1w/2pZYau7cKtSQePM/Wb+Vj8t3F9XbyRavOLgd/1Y6PUccEc5/8ce/BJjGcGlHH0T/7l2nUlpqsAIgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2f8bf1b9951192d713bc216bdc585df2')


line_bot_api = LineBotApi('jCCJTBH9PKP0UzrCtVCpT99E2kOPn3bowhUA8KX1hcxMHwqdZbfLzP/I6leONvKqZmNyqKC1w/2pZYau7cKtSQePM/Wb+Vj8t3F9XbyRavOLgd/1Y6PUccEc5/8ce/BJjGcGlHH0T/7l2nUlpqsAIgdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('2f8bf1b9951192d713bc216bdc585df2')



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
                TextSendMessage(text='Hey, thank you for inviting the MCOC Concierge In-Chat Bot. To get started type: Mc3 list'))
           
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
            
            
        #Whole List Breakdown    
        if event.message.text == "Mc3 list":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Mc3 aq"+'\n'+"Mc3 aw"+'\n'+"Mc3 arena"+'\n'+"Mc3 calendar"+'\n'+"Mc3 duels"+'\n'+"Mc3 mastery"+'\n'+"Mc3 prestige"+'\n'+"Mc3 special quests"))     
        
        #Specific List Breakdown, make sure to follow the headers identifying the class.
            #Aq Trigger
        if event.message.text == "Mc3 aq":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="aq boss practice"+'\n'+"aq costs"+'\n'+"aq maps"+'\n'+"aq rewards"))            
        
        #AQ Keywords
        if event.message.text == "Mc3 aq costs":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/BvLSyYt.jpg',
                    preview_image_url='https://example.com/preview.jpg'
                )
            )
                    
        if event.message.text == "Mc3 aq rewards":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/ZwdRIoj.jpg',
                    preview_image_url='https://example.com/preview.jpg'
                )
            )
            
        if event.message.text == "Mc3 boss practice":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/71x09Rm.jpg',
                    preview_image_url='https://example.com/preview.jpg'
                )
            )
            
        #AW Keywords    
        if event.message.text == "Mc3 aw map":
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://i.imgur.com/ZxgWTY7.jpg',
                    preview_image_url='https://example.com/preview.jpg'
                )
            )







if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
