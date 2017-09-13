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
from .models import UserConceptScore
from .models import UserQuestionScore
from .models import Concept
from .models import Test
from .al import LearningNew
from chatbot import chat_bot
from django.utils import timezone
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

    if UserConceptScore.objects.filter(user=request.user).count() == 0:
        con = Concept.objects.all()
        for c in con:
            ucs = UserConceptScore()
            ucs.user = request.user
            ucs.concept = c
            ucs.save()

    test = Test()
    test.user = request.user
    test.save()
    request.session['test_id'] = test.id

    learner = LearningNew()
    questionid, _ = learner.learn(-1, request, 0, 0)

    chatbot1 = chat_bot.ChatBot()

    qlist = chatbot1.get_dic(-1).keys()
    qlist9 = [str(i) for i in qlist]
    qlist9.sort()

    return render(request, 'index.html', {'questionid': questionid, 'qlist': qlist9})


def details(request, questionid):

    test = Test.objects.get(id=request.session['test_id'])

    if UserQuestionScore.objects.filter(user=request.user, test=test).count() == 0:

        que = QuestionBank.objects.all()
        for q in que:
            uqs = UserQuestionScore()
            uqs.user = request.user
            uqs.test = test
            uqs.question = q
            uqs.save()

    is_correct = 2
    next_id = None

    question = QuestionBank.objects.get(id=questionid)

    uqs = UserQuestionScore.objects.get(user=request.user, question=question, test=test)
    uqs.start_time = timezone.now()
    uqs.save()

    chatbot1 = chat_bot.ChatBot()

    qlist = chatbot1.get_dic(questionid).keys()
    qlist9 = [str(i) for i in qlist]
    qlist9.sort()

    im = chatbot1.main_bot(questionid, "InitialMessage", request)

    return render(request, "details.html", {'this_question': question, 'questionid': questionid,
                                            'is_correct': is_correct, 'next_id': next_id, 'qlist': qlist9,
                                            'im': im})


def check(request, questionid):

    question = get_object_or_404(QuestionBank, pk=questionid)
    users_answer = str(request.GET['Answer'])
    if question.answer == users_answer:
        is_correct = 1
    else:
        is_correct = 0

    test = Test.objects.get(id=request.session['test_id'])

    uqs = UserQuestionScore.objects.get(user=request.user, question=question, test=test)
    uqs.end_time = timezone.now()
    uqs.attempted = 1
    if is_correct == 1:
        uqs.correct = 1
    uqs.time_taken = (uqs.end_time - uqs.start_time).total_seconds()
    uqs.save()

    learner = LearningNew()
    next_id, result = learner.learn(questionid, request, uqs.time_taken, is_correct)

    q_level = question.level
    chatbot1 = chat_bot.ChatBot()
    qlist = chatbot1.get_dic(questionid).keys()
    qlist9 = [str(i) for i in qlist]
    qlist9.sort()

    t = round(uqs.time_taken, 2)

    if next_id == -2:
        request.session['result'] = result

    return render(request, "details.html", {'this_question':question, 'questionid':questionid,
                                            'is_correct': is_correct, 'next_id': next_id, 't': t,
                                            'q_level': q_level,
                                            'qlist': qlist9})


def result(request):

    return render(request, "analysis.html", {'result': request.session['result']})



