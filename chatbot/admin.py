# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import user_chat_log
from .models import qna_repository


admin.site.register(user_chat_log)
admin.site.register(qna_repository)
