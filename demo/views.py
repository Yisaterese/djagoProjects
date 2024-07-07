from django.shortcuts import render, HttpResponse


# Create your views here.

def say_hello(request):
    return HttpResponse("Hello, welcome to django")


def welcome(request, name):
    return HttpResponse(f" welcome, Mr {name}")


def say_hello2(request):
    return render(request, 'index.html', {"name":""})
