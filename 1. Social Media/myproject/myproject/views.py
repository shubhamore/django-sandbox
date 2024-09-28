# from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    # return HttpResponse('Hello world this is a homepage')
    return render(request, 'home.html')

def aboutpage(request):
    # return HttpResponse('Hello world this is an about page')
    return render(request, 'about.html')