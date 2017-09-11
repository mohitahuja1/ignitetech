from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


# Create your models here.


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_class = models.CharField(max_length=2000)
    user_board = models.CharField(max_length=2000)
    user_subject = models.CharField(max_length=2000)
    user_level = models.IntegerField(default=0)
    user_all = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)


class Test(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    result = models.CharField(max_length=2000, default="None")

    def __str__(self):
        return str(self.id)


class Concept(models.Model):

    concept = models.CharField(max_length=2000)
    concept_level = models.IntegerField(default=0)

    def __str__(self):
        return str(self.concept)


class QuestionBank(models.Model):

    question = models.CharField(max_length=2000)
    answer = models.CharField(max_length=2000)
    level = models.IntegerField(default=0)
    pct_users = models.FloatField(default=0.0)
    total_users = models.IntegerField(default=0)
    correct_time = models.FloatField(default=0.0)
    correct_users = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class UserConceptScore(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    asked = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)

    def __str__(self):
        return str(self.concept)


class UserQuestionScore(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)
    correct = models.IntegerField(default=0)
    attempt = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    time_taken = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.question)

