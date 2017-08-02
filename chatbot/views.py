from datetime import datetime
from django.shortcuts import render
from . import chat_bot
import logging
from django.views import generic
from django.http import HttpResponse
from .models import user_chat_log
logger = logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler(__name__),
                              logging.StreamHandler()])

def chat_index(request):
    user_id = 1
    users_question = request.GET.get("question", None)
    questionid = request.GET.get('question_id', None)
    bot_response = chat_bot.main_bot(questionid, users_question)
    chat_log = user_chat_log()
    chat_log.user_id = user_id
    chat_log.text_sent = users_question
    chat_log.text_recieved = bot_response
    chat_log.time_stamp = datetime.now()
    #chat_log.save()
    return HttpResponse(bot_response)