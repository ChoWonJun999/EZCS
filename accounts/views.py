from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User
import re
from django.http import HttpResponse
def login(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if not (username and password):
            result = '아이디와 비밀번호를 입력하세요'
        else:
            try:
                user = User.objects.get(username=username)
                if not user.is_active:
                    result = '관리자의 승인이 필요합니다.'
                elif password == user.password:
                    request.session['user'] = username
                    result = 'success'
                else:
                    result = '비밀번호가 올바르지 않습니다'
            except User.DoesNotExist:
                result = '해당 사용자가 존재하지 않습니다'
    else:
        result = 'request.method != POST'

    return JsonResponse({'result': result})

def logout(request):
    request.session.pop('user')
    return redirect('/')

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User

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
            user = User.objects.create(
                username=username,
                password=password,
                name=name,
                email=email,
                is_active=False  # 관리자 승인을 기다리는 상태로 설정
            )
            return redirect('/')  # 회원가입 성공 시 메인 페이지로 이동

    return render(request, 'accounts/signup.html', {'errors': errors})




def check_username(request):
    username = request.GET.get('username')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

def check_email(request):
    email = request.GET.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})
