import os
import sys
import linebot
from linebot import LineBotApi, WebhookParser
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError, InvalidSignatureError

line_bot_api = linebot.api.LineBotApi('jCCJTBH9PKP0UzrCtVCpT99E2kOPn3bowhUA8KX1hcxMHwqdZbfLzP/I6leONvKqZmNyqKC1w/2pZYau7cKtSQePM/Wb+Vj8t3F9XbyRavOLgd/1Y6PUccEc5/8ce/BJjGcGlHH0T/7l2nUlpqsAIgdB04t89/1O/w1cDnyilFU=')
parser = linebot.WebhookParser('2f8bf1b9951192d713bc216bdc585df2')

line_bot_api.push_message('<livingtribunal.davis>',TextSendMessage(text="hey"))
