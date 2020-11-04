from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return HttpResponse("<html><title>待办事项【To-Do lists】</title></html>")
