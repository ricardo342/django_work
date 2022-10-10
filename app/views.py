from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

'''建立一个http简单响应'''
def index(request):
    return HttpResponse('Hello World')
