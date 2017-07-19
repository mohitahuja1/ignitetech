"""

Important notes for Django:

1. source activate <VirtualEnvName> - starts virtual environment

2. source deactivate - stops virtual environment

3. python manage.py runserver - starts localhost server

4. python manage.py makemigrations - shows what changes are made in the database code

5. python manage.py migrate - makes those changes to the database

ALWAYS RUN THE ABOVE TWO WHEN CHANGING MODELS.PY
CHANGES IN DATABASE WILL BE RECORDED IN MIGRATIONS FOLDER

6. python manage.py syncdb - syncs database to latest changes made

7. postgresql and mysql are more secure than sqlite database

8. python manage.py createsuperuser - create a superuser and password to access admin console

9. python manage.py startapp - builds a folder that has a set of codes like adaptive learning or chatbot

10. python manage.py shell - allows us to edit the database through python scripts in terminal -
treating the models as a class. We can also use django specific commands to edit database.

"""

from django.shortcuts import render, get_object_or_404

from .models import question_bank

from . import util

from django.http import HttpResponse

import random

def index(request):

    first_question_id, _ = util.learn(-1)

    return render(request ,'index.html',{'first_question_id':first_question_id})

def details(request , questionid):

    this_question = get_object_or_404(question_bank, pk=questionid)

    is_correct = 2

    next_id = None

    return render(request, "details.html", {'this_question':this_question, 'is_correct':is_correct, 'next_id':next_id})

def check(request, questionid):

    this_question = get_object_or_404(question_bank, pk=questionid)

    users_answer = str(request.GET['Answer'])

    if (this_question.answer == users_answer):

        is_correct = 1

    else:

        is_correct = 0

    next_id, result = util.learn(this_question.id)

    if next_id == -2:

        return render(request, "analysis.html", {'result': result})

    else:

        return render(request, "details.html", {'this_question':this_question, 'is_correct':is_correct, 'next_id':next_id})

