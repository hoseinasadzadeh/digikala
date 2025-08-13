from django.shortcuts import render
from . import models


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def notFoundPage(request):
    return render(request, "404.html")
