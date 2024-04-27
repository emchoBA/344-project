from django.shortcuts import render
from django.http import HttpResponse

#initial values are set as -1 for easy error debug
user_age = -1
user_weight = -1
user_height = -1
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
    global user_age, user_weight, user_height
    user_age = request.POST.get('age')
    user_weight = request.POST.get('weight')
    user_height = request.POST.get('height')

    #text = foo()  ## get string from AI
    #context = {} ##use this to pass string text to displayinfo page
    return render(request, 'displayInfopage.html')

def dietReccomendationpage(request):
    return render(request, 'dietreccpage.html')