from datetime import datetime
from django.shortcuts import render
from . import chat_bot
import logging
from django.views import generic
from django.http import HttpResponse
from .models import user_chat_logs
logger = logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler(__name__),
                              logging.StreamHandler()])

# Create your views here.
def chat_index(request):
    logging.info({"request":request})
    user_id = 1
    users_question = request.GET.get("question", None)
    # data = request.GET.get('data', None)
    # user_question = data.get('question', None)
    questionid = request.GET.get('question_id', None)
    bot_response = chat_bot.main_bot(questionid, users_question)
    chat_log = user_chat_logs()
    chat_log.user_id = user_id
    chat_log.text_sent = users_question
    chat_log.text_recieved = bot_response
    chat_log.time_stamp = datetime.now()
    # bot_response = 'asdf'
    logging.info({"request_content": chat_log.text_sent, "questionid": questionid, "bot_reponse": chat_log.text_recieved,"time_stamp":chat_log.time_stamp})
    # return render(request , "chat/chat_index.html", {'bot_response':bot_response ,'users_question':users_question})
    return HttpResponse(bot_response)