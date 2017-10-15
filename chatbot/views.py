from datetime import datetime
from .chat_bot import ChatBot
import logging
from django.http import HttpResponse
from .models import UserChatLog
from .models import Topic
from .models import TopicRepository
import time


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
    time.sleep(1)
    return HttpResponse(bot_response)


def chat_revision(request):
    users_question = request.GET.get("question", None)
    for e in Topic.objects.values('topic'):
        if users_question == e['topic']:
            request.session['topic'] = e['topic']
    topic = request.session['topic']
    try:
        bot_response = TopicRepository.objects.get(topic=Topic.objects.get(topic=topic), doubt=users_question).answer
    except TopicRepository.DoesNotExist:
        bot_response = "Sorry! I couldn't understand. Please be more specific."

    chat_log = UserChatLog()
    chat_log.text_sent = users_question
    chat_log.text_recieved = bot_response
    chat_log.time_stamp = datetime.now()
    chat_log.save()
    time.sleep(1)

    return HttpResponse(bot_response)