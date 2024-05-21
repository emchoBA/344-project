from django.shortcuts import render

#from tidymeal import diet_recom
from django.http import HttpResponse
import joblib
import pandas as pd
import numpy
from random import uniform as rnd

from tidymeal.diet_recom import MealRecommender, custom_formatting

#initial values are set as 1 for easy error debug

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

    user_age = request.POST.get('age')
    user_weight = request.POST.get('weight')
    user_height = request.POST.get('height')
    user_activity = request.POST.get('activity')
    user_plan = request.POST.get('plan')

    activity_multiplier = 1
    plan_modifier = 0

    BRM = 88.362 + (13.397 * float(user_weight)) + (4.799 * float(user_height)) - (5.677 * float(user_age))

    match user_plan:
        case "low":
            plan_modifier = -300
        case "medium":
            plan_modifier = 300
        case "high":
            plan_modifier = 0

    match user_activity:
        case "none":
            activity_multiplier = 1.2
        case "light":
            activity_multiplier = 1.375
        case "moderate":
            activity_multiplier = 1.55
        case "active":
            activity_multiplier = 1.75

    calories = (BRM * activity_multiplier) + plan_modifier

    print(calories)
    recommender = MealRecommender("static/dataset.csv", "static/saved_model.sav")
    result_list = recommender.get_recommendations(calories) 
    breakfast_list, lunch_list, dinner_list = custom_formatting(result_list)

    context = {
        'breakfast_list': breakfast_list,
        'lunch_list': lunch_list,
        'dinner_list': dinner_list
    }

    return render(request, 'displayInfopage.html', context)


def dietReccomendationpage(request):
    return render(request, 'dietreccpage.html')
