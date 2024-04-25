from django.urls import path, include
from tinymeal import views
"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.say_hello),
    path('tinymeal/', views.say_hello),
    path('login/', views.login_page),
    path('register/', views.register_page),
    path('userhome/', views.user_home_page),
    path('displayInfo/', views.displayInfopage),
    path('dietrecc/', views.dietReccomendationpage)
]