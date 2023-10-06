from django.shortcuts import render
from django.http import HttpResponse


def showuser(request):
    return HttpResponse("Working Fine")
