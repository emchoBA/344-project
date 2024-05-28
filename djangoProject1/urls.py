# urls.py
from django.contrib import admin
from django.urls import path
from tidymeal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.say_hello, name='homepage'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('userhome/', views.user_home_page, name='userhome'),
    path('displayInfo/', views.displayInfopage, name='displayInfo'),
    path('dietrecc/', views.dietReccomendationpage, name='dietrecc'),
    path('api/register/', views.UserRegisterView.as_view(), name='api_register'),
    path('api/login/', views.UserLoginView.as_view(), name='api_login'),
    path('logout/', views.logout_view, name='logout'),
]
