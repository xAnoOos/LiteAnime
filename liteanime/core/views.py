from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to LiteAnime Home Page!")


def register(request):
    return HttpResponse("Register Page")

def thread_list(request):
    return HttpResponse("Thread Page")

def about(request):
    return HttpResponse("About Us Page")
