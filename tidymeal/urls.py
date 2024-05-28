# tidymeal/urls.py
from django.urls import path
from .views import UserRegisterView, UserLoginView, say_hello, login_page, register_page, user_home_page, displayInfopage, dietReccomendationpage

urlpatterns = [
    path('', say_hello, name='homepage'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('userhome/', user_home_page, name='userhome'),
    path('displayInfo/', displayInfopage, name='displayInfo'),
    path('dietreccomendation/', dietReccomendationpage, name='dietreccomendation'),
    path('api/register/', UserRegisterView.as_view(), name='api_register'),
    path('api/login/', UserLoginView.as_view(), name='api_login'),
]
