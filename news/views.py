from rest_framework import generics, permissions,serializers
from .models import News, NewsComment
from .serializers import NewsSerializer, NewsCommentSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from core.models import Notification
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseForbidden
from rest_framework.response import Response









class NewsListCreateView(generics.ListCreateAPIView):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer

    def get_permissions(self):
        return [permissions.AllowAny()]

    def perform_create(self, serializer):

        title = self.request.data.get("title", "").strip()
        content = self.request.data.get("content", "").strip()

        if not title or not content:
            raise serializers.ValidationError("Title and content are required.")

        serializer.save(user=self.request.user)
    
class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class NewsCommentCreateView(generics.CreateAPIView):
    queryset = NewsComment.objects.all()
    serializer_class = NewsCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        news = News.objects.get(pk=self.kwargs['pk'])
        parent_id = self.request.data.get("parent")

        comment = serializer.save(user=self.request.user, news=news, parent_id=parent_id or None)

        if news.user != self.request.user:
            Notification.objects.create(
                recipient=news.user,
                sender=self.request.user,
                message=f"{self.request.user.username} commented on your news: {news.title}",
                url=self.request.build_absolute_uri(reverse('news_detail_page', args=[news.pk]))
            )

        if parent_id:
            parent = NewsComment.objects.filter(pk=parent_id).first()
            if parent and parent.user != self.request.user:
                Notification.objects.create(
                    recipient=parent.user,
                    sender=self.request.user,
                    message=f"{self.request.user.username} replied to your comment",
                    url=self.request.build_absolute_uri(reverse('news_detail_page', args=[news.pk]))
                )
@csrf_protect
@login_required
def create_news_page(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("❌ You are not authorized to post news.")
    return render(request, 'create_news.html')

@login_required
def news_detail_page(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news_detail.html', {'news': news})


def news_list_page(request):
    all_news = News.objects.all().order_by('-created_at')
    return render(request, 'news.html', {'news': all_news})