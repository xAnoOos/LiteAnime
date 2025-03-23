from django.contrib import admin
from .models import Profile, Thread, Comment, User

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_image')  
    search_fields = ('user__username',)  

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')  
    search_fields = ('title', 'user__username')    
    list_filter = ('created_at',)  

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'thread', 'created_at')  
    search_fields = ('user__username', 'thread__title')  
    list_filter = ('created_at',)  


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment, CommentAdmin)
