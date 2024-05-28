from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, TokenSerializer
from tidymeal.diet_recom import MealRecommender, custom_formatting

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
    if request.user.is_authenticated:
        return redirect('userhome')
    return render(request, 'homepage.html')

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)  # Düzeltme: username=email
        if user is not None:
            login(request, user)
            return redirect('userhome')
        else:
            return render(request, 'loginscreen.html', {'error': 'Invalid username or password'})
    return render(request, 'loginscreen.html')

def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('userhome')
    else:
        form = UserCreationForm()
    return render(request, 'createacc.html', {'form': form})

@login_required
def user_home_page(request):
    context = {'username': request.user.username}
    return render(request, 'userhomepage.html', context)

@login_required
def displayInfopage(request):
    if request.method == 'POST':
        user_age = request.POST.get('age')
        user_weight = request.POST.get('weight')
        user_height = request.POST.get('height')
        user_activity = request.POST.get('activity')
        user_plan = request.POST.get('plan')

        calculator = UserCalorieCalculator(user_age, user_weight, user_height, user_activity, user_plan)
        calories = calculator.calculate_calories()

        recommender = MealRecommender("static/dataset.csv", "static/saved_model.sav")
        result_list = recommender.get_recommendations(calories) 
        breakfast_list, lunch_list, dinner_list = custom_formatting(result_list)

        context = {
            'breakfast_list': breakfast_list,
            'lunch_list': lunch_list,
            'dinner_list': dinner_list,
            'calories': calories,
            'username': request.user.username,
            'plan': user_plan
        }

        return render(request, 'displayInfopage.html', context)
    context = {'username': request.user.username}
    return render(request, 'dietreccpage.html', context)

@login_required
def dietReccomendationpage(request):
    context = {'username': request.user.username}
    return render(request, 'dietreccpage.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

class UserRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

class UserLoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
