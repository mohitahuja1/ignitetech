from django.db import models
from django.conf import settings

# Create your models here.

class Test(models.Model):

    test = models.IntegerField(default=0)

    def __str__(self):
        return str(self.test)

class QuestionBank(models.Model):

    test = models.ForeignKey(Test, on_delete=models.CASCADE)
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
    concept_id = models.IntegerField(default=0)
    read = models.IntegerField(default=0)
    corrects = models.IntegerField(default=0)
    incorrects = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

class UserQuestionScore(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)
    correct = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)
