from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from module import func, funcresult


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '@AQI_help':
                        func.helpAQI(event)
                    elif mtext == '@RATE_help':
                        func.helpRAET(event)                         
                    else:
                        #text = '不好意思，目前沒有完全符合您提問的答案，建議您換個方式描述或是一次詢問單一問題，或許我就能回答您喔，謝謝!!!'
                        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text))
                        funcresult.search(event, mtext)
                        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()