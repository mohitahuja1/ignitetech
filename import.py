
import csv, sys, os

project_dir = "/Users/pallaviahuja/Dropbox/Ignite \Tech/Tech/code/web_app/ignitetech/ignitetech"

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ignitetech.settings'

import django

django.setup()

from chatbot.models import qna_repository

# Load qna repository into database

data = csv.reader(open('/Users/pallaviahuja/Dropbox/Ignite Tech/Tech/rawdata/qna_rep.csv'),delimiter = ",", quotechar = '"')

for e in data:
    if e[0] != "Sno":
        qna = qna_repository()
        qna.question_id = e[0]
        qna.q = e[1]
        qna.a = e[2]
        qna.save()