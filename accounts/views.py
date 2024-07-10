from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import logging


logger = logging.getLogger(__name__)


def user_login(request):
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
            counselor = CounselorProfile.objects.filter(auth_user_id=user.id).first()
            admin = AdministratorProfile.objects.filter(auth_user_id=user.id).first()

            if (counselor and counselor.active_status != 1) or (admin and admin.active_status != 1):
                result = '로그인 권한이 없습니다.'
            else:
                login(request, user)
                request.session['user'] = user.first_name if user.first_name else user.username

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


def user_logout(request):
    """
        로그아웃
    """
    logout(request)
    request.session.pop('user', None)
    return redirect('/')


def adminLogin(request):
    return render(request, 'accounts/adminlogin.html')


def searchPW(request):
    return render(request, 'accounts/searchpw.html')



def signup(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        birth_date = request.POST.get('birthdate')
        address_code = request.POST.get('addressCode')
        address = request.POST.get('address')
        address_detail = request.POST.get('addressDetail')
        print("aaaaaaaaaaaaaaaaaaaaaaaa")
        
        if not username or not password or not name or not phone_number or not email or not birth_date or not address_code or not address or not address_detail:
            return JsonResponse({'result': False, 'msg': '모든 필드를 입력해 주세요.'})
    
        user = User.objects.create_user(
            username = username,
            password = password,
            first_name = name,
            email = email,
        )
        
        CounselorProfile.objects.create(
            auth_user=User.objects.get(id=user.id)
            , birth_date=birth_date
            , phone_number=phone_number
            , address_code=address_code
            , address=address
            , address_detail=address_detail
            # , department=department
            # , active_status=active_status
        )

        result = True
        msg = "회원가입 요청이 완료되었습니다."

        return JsonResponse({'result': result, 'msg': msg})


def check_username(request):
    username = request.POST.get('username')
    is_taken = User.objects.filter(username=username).exists()
    print(is_taken)
    return JsonResponse({'is_taken': is_taken})

def check_email(request):
    email = request.GET.get('email')
    is_taken = User.objects.filter(email=email).exists()
    return JsonResponse({'is_taken': is_taken})

def check_phone(request): 
    phone_number = request.GET.get('phone_number')
    is_taken = CounselorProfile.objects.filter(phone_number=phone_number).exists()
    return JsonResponse({'is_taken': is_taken})

def searchPW(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        birthdate = request.POST.get('birthdate')
        phone_number = request.POST.get('phone_number')

        try:
            user = User.objects.get(username=username)
            counselor_profile = CounselorProfile.objects.get(auth_user=user, birth_date=birthdate, phone_number=phone_number)
            # 인증 정보가 맞다면 비밀번호 재설정 페이지로 이동
            request.session['reset_user_id'] = user.id
            return JsonResponse({'result': 'success', 'msg': '인증 성공. 비밀번호를 재설정해주세요.'})
        except (User.DoesNotExist, CounselorProfile.DoesNotExist):
            return JsonResponse({'result': 'error', 'msg': '해당 정보의 사용자를 찾을 수 없습니다.'})
    return render(request, 'accounts/searchPW.html')

def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user_id = request.session.get('reset_user_id')

        try:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            del request.session['reset_user_id']
            return JsonResponse({'result': 'success', 'msg': '비밀번호가 성공적으로 변경되었습니다.'})
        except User.DoesNotExist:
            return JsonResponse({'result': 'error', 'msg': '사용자를 찾을 수 없습니다.'})
    return render(request, 'accounts/reset_password.html')