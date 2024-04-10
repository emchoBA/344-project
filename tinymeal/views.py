from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request):
    return render(request, 'homepage.html')
# Create your views here.

def login_page(request):
    return render(request, 'loginscreen.html')