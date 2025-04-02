from rest_framework import serializers
from .models import News, NewsComment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class NewsCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = NewsComment
        fields = ['id', 'user', 'content', 'parent', 'created_at', 'replies']

    def get_replies(self, obj):
        if obj.replies.exists():
            return NewsCommentSerializer(obj.replies.all(), many=True).data
        return []

class NewsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = NewsCommentSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image', 'created_at', 'user', 'comments']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        return News.objects.create(user=user, **validated_data)