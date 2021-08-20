from django.contrib import admin

from .models import TaskToMemorize, Review

from learn_algoritms_bot.models import TelegramUser

admin.site.register(TaskToMemorize)
admin.site.register(Review)
admin.site.register(TelegramUser)
