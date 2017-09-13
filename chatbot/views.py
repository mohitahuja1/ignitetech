from datetime import datetime
from .chat_bot import ChatBot
import logging
from django.http import HttpResponse
from .models import UserChatLog

logger = logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler(__name__),
                              logging.StreamHandler()])


def chat_index(request):
    users_question = request.GET.get("question", None)
    questionid = request.GET.get('question_id', None)
    chatbot1 = ChatBot()
    bot_response = chatbot1.main_bot(questionid, users_question, request)
    chat_log = UserChatLog()
    chat_log.text_sent = users_question
    chat_log.text_recieved = bot_response
    chat_log.time_stamp = datetime.now()
    chat_log.save()
    return HttpResponse(bot_response)