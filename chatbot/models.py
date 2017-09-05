# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from adaptive_learning.models import QuestionBank
from adaptive_learning.models import Concept


# Create your models here.

class UserChatLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    text_sent = models.CharField(max_length=2000)
    text_recieved = models.CharField(max_length=2000)
    time_stamp= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class QnaRepository(models.Model):

    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, default=1)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, default=1)
    doubt = models.CharField(max_length=2000)
    answer = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.id)

