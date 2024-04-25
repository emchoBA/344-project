from django.urls import path
from . import views

urlpatterns = [
    path('', views.say_hello),
    path('/login', views.login_page),
    path('/register', views.register_page),
    path('/userhome', views.user_home_page),
    path('/displayInfo', views.displayInfopage),
    path('/dietrecc', views.dietReccomendationpage)
]