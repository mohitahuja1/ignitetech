
from django.contrib import admin

# Register your models here.

from .models import QuestionBank
from .models import UserConceptScore
from .models import Test
from .models import UserQuestionScore


admin.site.register(QuestionBank)
admin.site.register(UserConceptScore)
admin.site.register(Test)
admin.site.register(UserQuestionScore)
