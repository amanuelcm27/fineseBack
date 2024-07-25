from django.shortcuts import render, HttpResponse

# Create your views here.


def starter(request):
    return HttpResponse("Hello, Finese")