# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import UserChatLog
from .models import QnaRepository


admin.site.register(UserChatLog)
admin.site.register(QnaRepository)
