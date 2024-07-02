from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import re
from django.http import HttpResponse
import logging
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


def login(request):
    if request.method == 'GET':
        # 추가
        context = {}
        if 'remember_me' in request.COOKIES:
            context['username'] = request.COOKIES['remember_me']
            context['remember_me'] = True  
        return render(request, 'accounts/login.html', context)

    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        remember_me = request.POST.get('remember_me', None)
        

        if not (username and password):
            result = '아이디와 비밀번호를 입력하세요'
        else:
            try:
                user = User.objects.get(username=username)
                if not user.is_active:
                    result = '관리자의 승인이 필요합니다.'
                elif password == user.password:
                    request.session['user'] = username
                    if user.is_superuser == True:
                        result = 'manager'
                    else:
                        result = 'user'
                    # 수정
                    response = JsonResponse({'result' : result})
                    if remember_me == 'on':
                        response.set_cookie('remember_me', username, max_age=2592000)
                    else:
                        response.delete_cookie('remember_me')
                    return response
                else:
                    result = '비밀번호가 올바르지 않습니다'
            except User.DoesNotExist:
                result = '해당 사용자가 존재하지 않습니다'
    return JsonResponse({'result': result})

def logout(request):
    auth_logout(request)
    #request.session.pop('user')
    return redirect('/')


def searchPW(request):
    return render(request, 'accounts/searchpw.html')


def signup(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        name = request.POST.get('name')
        email = request.POST.get('email')

        if not username:
            errors['username'] = '사용자명을 입력하세요.'
        elif User.objects.filter(username=username).exists():
            errors['username'] = '이미 존재하는 사용자명입니다.'

        if not password:
            errors['password'] = '비밀번호를 입력하세요.'
        else:
            try:
                password_validation.validate_password(password, User)
            except ValidationError as e:
                errors['password'] = ', '.join(e.messages)
        
        if not password_confirm:
            errors['password_confirm'] = '비밀번호 확인을 입력하세요.'
        elif password != password_confirm:
            errors['password_confirm'] = '입력된 비밀번호가 다릅니다.'

        if not name:
            errors['name'] = '이름을 입력하세요.'

        if not email:
            errors['email'] = '이메일을 입력하세요.'
        elif User.objects.filter(email=email).exists():
            errors['email'] = '이미 존재하는 이메일입니다.'

        if not errors:
            user = User.objects.create_user(
            #user = User.objects.create(
                username=username,
                password=password,
                name=name,
                email=email,
                #is_active=0
            )
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'errors': errors})

    return render(request, 'accounts/signup.html')

def check_username(request):
    username = request.GET.get('username')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})


def check_email(request):
    email = request.GET.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})
