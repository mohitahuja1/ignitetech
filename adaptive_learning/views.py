from django.shortcuts import render, get_object_or_404

from .models import question_bank

from . import util

from django.http import HttpResponse

import random

# Create your views here.

def index(request):

    first_question_id, _ = util.function1(-1)

    return render(request ,'index.html',{'first_question_id':first_question_id})

def details(request , questionid):

    return render(request , "details.html")