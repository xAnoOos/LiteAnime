from django.contrib import admin
from .models import Profile, Thread, Comment, User
from django.utils.html import format_html


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_avatar')

    def profile_avatar(self, obj):
        return format_html('<img src="{}" width="40" height="40" style="border-radius:50%"/>', obj.avatar.url)
    profile_avatar.short_description = 'Avatar'

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')  
    search_fields = ('title', 'user__username')    
    list_filter = ('created_at',)  

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'thread', 'created_at')  
    search_fields = ('user__username', 'thread__title')  
    list_filter = ('created_at',)  


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment, CommentAdmin)
