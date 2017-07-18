from django.db import models

# Create your models here.

class question_bank(models.Model):
    question = models.CharField(max_length=2000)
    answer = models.CharField(max_length=2000)
    pct_users = models.FloatField(default = 0.0)
    total_users = models.IntegerField(default = 0)
    correct_time = models.FloatField(default = 0.0)
    correct_users = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.id)
