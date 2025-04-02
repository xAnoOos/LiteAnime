from django.contrib import admin

from .models import News, NewsComment

admin.site.register(News)
admin.site.register(NewsComment)
