from django.shortcuts import render

#from tidymeal import diet_recom
from django.http import HttpResponse
import joblib
import pandas as pd
import numpy
from random import uniform as rnd

from tidymeal.diet_recom import MealRecommender, custom_formatting

#initial values are set as 1 for easy error debug
# utils.py

class UserCalorieCalculator:
    def __init__(self, age, weight, height, activity, plan):
        self.age = float(age)
        self.weight = float(weight)
        self.height = float(height)
        self.activity = activity
        self.plan = plan
        self.activity_multiplier = 1
        self.plan_modifier = 0

    def calculate_bmr(self):
        return 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)

    def set_activity_multiplier(self):
        match self.activity:
            case "none":
                self.activity_multiplier = 1.2
            case "light":
                self.activity_multiplier = 1.375
            case "moderate":
                self.activity_multiplier = 1.55
            case "active":
                self.activity_multiplier = 1.75

    def set_plan_modifier(self):
        match self.plan:
            case "low":
                self.plan_modifier = -300
            case "medium":
                self.plan_modifier = 300
            case "high":
                self.plan_modifier = 0

    def calculate_calories(self):
        self.set_activity_multiplier()
        self.set_plan_modifier()
        bmr = self.calculate_bmr()
        return (bmr * self.activity_multiplier) + self.plan_modifier

def say_hello(request):
    return render(request, 'homepage.html')

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

    calculator = UserCalorieCalculator(user_age, user_weight, user_height, user_activity, user_plan)
    calories = calculator.calculate_calories()

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
