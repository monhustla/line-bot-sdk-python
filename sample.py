import os
import sys
import wsgiref.simple_server
from linebot import LineBotApi
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import LineBotApiError
from argparse import ArgumentParser
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.utils import PY3

channel_secret = os.getenv('Line_Channel_Secret', None)
channel_access_token = os.getenv('Line_Channel_Access_Token', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    

line_bot_api=LineBotApi(channel_access_token)
parser= WebhookParser(channel_secret)

def application(environ, start_response):
    # check request path
    if environ['PATH_INFO'] != '/callback':
        start_response('404 Not Found', [])
        return create_body('Not Found')

    # check request method
    if environ['REQUEST_METHOD'] != 'POST':
        start_response('405 Method Not Allowed', [])
        return create_body('Method Not Allowed')

    # get X-Line-Signature header value
    signature = environ['HTTP_X_LINE_SIGNATURE']

    # get request body as text
    wsgi_input = environ['wsgi.input']
    content_length = int(environ['CONTENT_LENGTH'])
    body = wsgi_input.read(content_length).decode('utf-8')

    try:
        events=parser.parse(body,signature)
    except InvalidSignatureError:
        start_response('400 Bad Request',[])
        return create_body ('Bad Request')
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
    
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='hey'))

    start_response('200 OK', [])
    return create_body('OK')

def create_body(text):
    if PY3:
        return [bytes(text, 'utf-8')]
    else:
        return text


if __name__ == '__main__':
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    options = arg_parser.parse_args()

    httpd = wsgiref.simple_server.make_server('', options.port, application)
    httpd.serve_forever()
