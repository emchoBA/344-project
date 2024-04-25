from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request):
    return render(request, 'homepage.html')
# Create your views here.

def login_page(request):
    return render(request, 'loginscreen.html')

def register_page(request):
    return render(request, 'createacc.html')

def user_home_page(request):
    return render(request, 'userhomepage.html')

def displayInfopage(request):
    return render(request, 'displayInfopage.html')

def dietReccomendationpage(request):
    return render(request, 'dietreccpage.html')