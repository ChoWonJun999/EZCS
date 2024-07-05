from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import re
import logging
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

def login_pass(request):
    username = request.POST.get('username', None)
    if username == "test":
        request.session['user'] = username
        return JsonResponse({'result' : 'all'})

def login(request):
    """
        request.method == 'GET': 접속
        request.method == 'POST': 로그인/관리자 로그인
        request.method == *: 잘못된 접근
    """

    if request.method == 'GET':
        context = {}
        if 'remember_me' in request.COOKIES:
            context['username'] = request.COOKIES['remember_me']
            context['remember_me'] = True  
        return render(request, 'accounts/login.html', context)
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        remember_me = request.POST.get('remember_me', None)

        user = authenticate(request, username=username, password=password)
        logger.log(1, user)

        if user is not None:
            if user.active_status != 1:
                result = '로그인 권한이 없습니다.'
            else:
                auth_login(request, user)
                request.session['user'] = user.name
                if user.is_superuser == True:
                    result = 'manager'
                else:
                    result = 'user'
                
                response = JsonResponse({'result' : result})
                if remember_me == 'on':
                    response.set_cookie('remember_me', username, max_age=2592000)
                else:
                    response.delete_cookie('remember_me')
                return response
        else:
            result = 'ID 혹은 PW를 확인해 주세요.'
    else:
        result = '잘못된 접근입니다.'
    return JsonResponse({'result': result})


def logout(request):
    """
        로그아웃
    """
    auth_logout(request)
    return redirect('/')


def adminLogin(request):
    return render(request, 'accounts/adminlogin.html')


def searchPW(request):
    return render(request, 'accounts/searchpw.html')



def signup(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        result = True
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        birth_date = request.POST.get('birthdate')
        address_code = request.POST.get('addressCode')
        address = request.POST.get('address')
        address_detail = request.POST.get('addressDetail')

        User.objects.create_user(
            username = username,
            password = password,
            name = name,
            email = email,
            birth_date = birth_date,
            phone_number = phone_number,
            address_code = address_code,
            address = address,
            address_detail = address_detail
        )
        msg = "회원가입 요청이 완료되었습니다."
    else:
        result = False
        msg = '잘못된 접근입니다.'

    return JsonResponse({'result': result, 'msg': msg})


def check_username(request):
    username = request.GET.get('username')
    is_taken = User.objects.filter(username=username).exists()
    return JsonResponse({'is_taken': is_taken})

def check_email(request):
    email = request.GET.get('email')
    is_taken = User.objects.filter(email=email).exists()
    return JsonResponse({'is_taken': is_taken})

def check_phone(request): 
    phone_number = request.GET.get('phone_number')
    is_taken = User.objects.filter(phone_number=phone_number).exists()
    return JsonResponse({'is_taken': is_taken})

