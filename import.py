
import csv
import sys
import os
import django

project_dir = "/Users/pallaviahuja/Dropbox/Ignite \Tech/Tech/code/web_app/ignitetech/ignitetech"

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ignitetech.settings'

django.setup()

# Load concept repository into database

# from adaptive_learning.models import Concept
#
#
# data = csv.reader(open('/Users/pallaviahuja/Dropbox/Ignite Tech/Tech/rawdata/concepts_raw.csv'), delimiter=",",
#                   quotechar='"')
#
# for e in data:
#     if e[0] != "concept":
#         con = Concept()
#         con.concept = e[0]
#         con.concept_level = e[1]
#         con.save()
#
#
# # Load question repository into database
#
# from adaptive_learning.models import QuestionBank
#
#
# data = csv.reader(open('/Users/pallaviahuja/Dropbox/Ignite Tech/Tech/rawdata/questionbank.csv'), delimiter=",",
#                   quotechar='"')
#
# for e in data:
#     if e[0] != "question":
#         que = QuestionBank()
#         que.question = e[0]
#         que.answer = e[1]
#         que.level = e[2]
#         que.save()
#
# # Load qna repository into database

from adaptive_learning.models import Concept
from adaptive_learning.models import QuestionBank
from chatbot.models import QnaRepository

data = csv.reader(open('/Users/pallaviahuja/Dropbox/Ignite Tech/Tech/rawdata/qcd_raw.csv'), delimiter=",",
                  quotechar='"')

for e in data:
    if e[0] != "question":
        qna = QnaRepository()
        qna.question = QuestionBank.objects.get(question=e[0])
        qna.concept = Concept.objects.get(concept=e[1])
        qna.doubt = e[2]
        qna.answer = e[3]
        qna.save()

# from chatbot.models import Topic
#
# data = csv.reader(open('/Users/pallaviahuja/Dropbox/Ignite Tech/Tech/rawdata/topic_raw.csv'), delimiter=",",
#                   quotechar='"')
#
# for e in data:
#     if e[0] != "topic":
#         t = Topic()
#         t.topic = e[0]
#         t.save()
#
# from chatbot.models import TopicRepository
# from adaptive_learning.models import Concept
# from chatbot.models import Topic
#
#
# data = csv.reader(open('/Users/pallaviahuja/Dropbox/Ignite Tech/Tech/rawdata/tcd_raw.csv'), delimiter=",",
#                   quotechar='"')
#
# for e in data:
#     if e[0] != "topic":
#         tr = TopicRepository()
#         tr.topic = Topic.objects.get(topic=e[0])
#         tr.concept = Concept.objects.get(concept=e[1])
#         tr.doubt = e[2]
#         tr.answer = e[3]
#         tr.save()