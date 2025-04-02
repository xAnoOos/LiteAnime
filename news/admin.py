from django.contrib import admin
from .models import News, NewsComment

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']
    exclude = ['user']  

    def save_model(self, request, obj, form, change):
        if not obj.pk:  
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(News, NewsAdmin)
admin.site.register(NewsComment)
