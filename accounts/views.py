<<<<<<< HEAD
# from django.shortcuts import render

# def list(request):
#     return render(request, 'accounts/Login.html')

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # 회원가입 후 리디렉션할 페이지
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # 로그인 후 리디렉션할 페이지
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # 로그아웃 후 리디렉션할 페이지
=======
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User

def login(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        
        if not (username and password):
            result = '데이터가 안들어옴'
        else:
            try:
                user = User.objects.get(username=username)
                if password == user.password:
                    request.session['user'] = username
                    result = 'success'
                else:
                    result = 'Incorrect password'
            except User.DoesNotExist:
                result = 'User does not exist'
    else:
        result = 'request.method != POST'

    return JsonResponse({'result': result})

def logout(request):
    request.session.pop('user')
    return redirect('/')
>>>>>>> 8e63f706690a8a255cbdf7dcb00b2165fa563487
