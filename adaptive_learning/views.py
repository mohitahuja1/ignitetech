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

from django.shortcuts import render, redirect, get_object_or_404
from .models import QuestionBank
from .al import learning
from chatbot import chat_bot
import time
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def index(request):

    global learning1
    learning1 = learning(levels = 4)
    questionid,_,_,_ = learning1.learn(-1,0,[],[],0)
    chatbot1 = chat_bot.ChatBot()
    qlist = chatbot1.get_dic(-1).keys()
    qlist9 = [str(i) for i in qlist]
    qlist9.sort()
    return render(request, 'index.html', {'questionid': questionid, 'qlist': qlist9})

def details(request , questionid):

    global learning1
    questionid = int(questionid)
    questionid += 1
    questionid = str(questionid)
    this_question = get_object_or_404(QuestionBank, pk=questionid)
    questionid = int(questionid)
    questionid -= 1
    is_correct = 2
    next_id = None
    learning1.tm[questionid][0] = time.time()
    chatbot1 = chat_bot.ChatBot()
    qlist = chatbot1.get_dic(questionid).keys()
    qlist9 = [str(i) for i in qlist]
    qlist9.sort()
    return render(request, "details.html", {'this_question':this_question, 'questionid':questionid, 'is_correct':is_correct, 'next_id':next_id, 'qlist':qlist9})

def check(request, questionid):

    global learning1
    questionid = int(questionid)
    questionid += 1
    questionid = str(questionid)
    this_question = get_object_or_404(QuestionBank, pk=questionid)
    questionid = int(questionid)
    questionid -= 1
    learning1.tm[questionid][1] = time.time()
    users_answer = str(request.GET['Answer'])
    user_metric = [this_question.pct_users, this_question.total_users]
    time_metric = [this_question.correct_time, this_question.correct_users]

    if (this_question.answer == users_answer):
        is_correct = 1
    else:
        is_correct = 0
    t = learning1.tm[questionid][1] - learning1.tm[questionid][0]
    t = round(t,2)

    next_id, result, user_metric, time_metric = learning1.learn(questionid, t, user_metric, time_metric, is_correct)

    this_question.pct_users = user_metric[0]
    this_question.total_users = user_metric[1]
    this_question.correct_time = time_metric[1]
    this_question.correct_users = time_metric[1]
    this_question.save()

    q_level = learning1.q_level[questionid]
    chatbot1 = chat_bot.ChatBot()
    qlist = chatbot1.get_dic(questionid).keys()
    qlist9 = [str(i) for i in qlist]
    qlist9.sort()

    if next_id == -2:
        return render(request, "analysis.html", {'result': result})
    else:
        return render(request, "details.html", {'this_question':this_question, 'questionid':questionid, 'is_correct':is_correct, 'next_id':next_id,'t':t, 'q_level': q_level, 'qlist':qlist})

