from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import re
import logging
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


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
            if not user.is_active:
                result = '관리자의 승인이 필요합니다.'
            else:
                auth_login(request, user)
                request.session['user'] = username
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
            result = '해당 사용자가 존재하지 않습니다'
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


def validate_username(username):
    if re.search(r'[ㄱ-ㅎㅏ-ㅣ가-힣]', username):
        raise ValidationError('아이디는 한글을 포함할 수 없습니다.')


def validate_name(name):
    if not re.match(r'^[가-힣]+$', name):
        raise ValidationError('이름은 한글만 포함해야 합니다.')
    

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
        else:
            try:
                validate_username(username)
            except ValidationError as e:
                errors['username'] = str(e)

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
        else:
            try:
                validate_name(name)
            except ValidationError as e:
                errors['name'] = str(e)

        if not email:
            errors['email'] = '이메일을 입력하세요.'
        elif User.objects.filter(email=email).exists():
            errors['email'] = '이미 존재하는 이메일입니다.'

        if not errors:
            user = User.objects.create_user(
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

