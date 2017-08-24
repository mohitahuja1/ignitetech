# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserChatLog(models.Model):
    user_id=models.IntegerField()
    text_sent = models.CharField(max_length=2000)
    text_recieved = models.CharField(max_length=2000)
    time_stamp= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class QnaRepository(models.Model):
    question_id=models.IntegerField()
    q = models.CharField(max_length=2000)
    a = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.q)

