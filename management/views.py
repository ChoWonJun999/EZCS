from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .models import Board
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def board_delete(request, id):
    board = get_object_or_404(Board, id=id)
    board.delete()
    return redirect('management:board_list')

def validate_image(file):
    valid_mime_types = ['image/jpeg', 'image/png']
    if file.content_type not in valid_mime_types:
        raise ValidationError('jpg, jpeg, and png 파일만 업로드 가능합니다.')


def mask_name(full_name):
    if len(full_name) <= 2:
        return full_name[:-1] + '*'
    else:
        return full_name[0] + '*' * (len(full_name) - 2) + full_name[-1]
    
def list(request, flag):
    search_select = request.GET.get("searchSelect", "")
    search_text = request.GET.get("searchText", "")
    start_date = request.GET.get("startDate", "")
    end_date = request.GET.get("endDate", "")
    query = Q()

    if flag == 'm':
        query &= Q(auth_user__is_superuser=False)
        query |= Q(active_status=1)
        query |= Q(active_status=2)
        query |= Q(active_status=3)
    elif flag == 'ad':
        query &= Q(auth_user__is_superuser=True)
    elif flag == 'board':
        boards = Board.objects.all()
        context = {'boards': boards}
        return render(request, 'management/board_list.html', context)
    else:
        query &= Q(auth_user__is_superuser=False)
        query &= Q(active_status=0)
    
    query1 = Q()
    if search_select:
        valid_fields = {
            'name': 'auth_user__first_name__icontains',
            'id': 'auth_user__username__icontains',
            'email': 'auth_user__email__icontains',
        }

        if search_select == 'all':
            for val in valid_fields.values():
                query1 |= Q(**{val: search_text})
        else:
            search_field = valid_fields[search_select]
            query1 = Q(**{search_field: search_text})

    query2 = Q()
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
        
        query2 &= Q(auth_user__date_joined__gte=start_date)
        query2 &= Q(auth_user__date_joined__lte=end_date)
    else:
        one_month_ago = datetime.now() - timedelta(days=30)
        query2 &= Q(auth_user__date_joined__gte=one_month_ago)
        query2 &= Q(auth_user__date_joined__lte=datetime.now())
        start_date = one_month_ago.strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

    if flag == 'ad':
        data = AdministratorProfile.objects.filter(query & query1 & query2)
    else:
        data = CounselorProfile.objects.filter(query & query1 & query2)
    
    paginator = Paginator(data, 10)
    page = request.GET.get('page')
    data = paginator.get_page(page)
    
    for profile in data:
        profile.masked_name = mask_name(profile.auth_user.first_name)

    context = {
        'flag': flag,
        'data': data,
        'searchSelect': search_select,
        'searchText': search_text,
        'startDate': start_date,
        'endDate': end_date,
        'is_paginated': data.has_other_pages(),
    }

    return render(request, 'management/list.html', context)

def board_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        flag = request.POST.get('flag', 0)  # 기본값으로 활성화 상태 설정

        # 파일 형식 검증
        if 'file' in request.FILES:
            file = request.FILES['file']
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in ['jpg', 'jpeg', 'png']:
                return render(request, 'management/board_create.html', {'error': '파일 형식이 유효하지 않습니다. jpg, jpeg, png 형식만 업로드 가능합니다.'})

        board = Board.objects.create(
            auth_user=request.user,
            title=title,
            body=body,
            flag=flag
        )

        if 'file' in request.FILES:
            board.file = request.FILES['file']
            board.save()

        return redirect('management:board_list')  # 공지사항 목록 페이지로 리디렉션
    return render(request, 'management/board_create.html')

def board_list(request):
    boards = Board.objects.all()
    return render(request, 'management/board_list.html', {'boards': boards})

def board_detail(request, id):
    board = get_object_or_404(Board, id=id)
    return render(request, 'management/board_detail.html', {'board': board})

def detail(request, id, flag):
    """
    유저 상세 페이지
    
    """
    if flag == 'ad':
        data = get_object_or_404(AdministratorProfile, id=id)
    else:
        data = get_object_or_404(CounselorProfile, id=id)

    context = {
        'flag': flag,
        'data': data
    }
    return render(request, 'management/detail.html', context)

def update_auth(request, id, status):
    """
    UPDATE counselor_profile SET active_status = ?
    """
    user = CounselorProfile.objects.get(id=id)
    user.active_status = status
    user.save()
    
    flag = 'm'
    if status == 1:
        flag = 'a'

    return redirect('management:list', flag)


def edit(request, id, flag):
    """
    개인정보 수정
    """
    if flag == 'ad':
        user_profile = get_object_or_404(AdministratorProfile, id=id)
    else:
        user_profile = get_object_or_404(CounselorProfile, id=id)
        
    auth_user = user_profile.auth_user
    
    if request.method == 'GET':
        context = {
            'flag': flag,
            'user': user_profile
        }
        return render(request, 'management/edit.html', context)
    else:
        auth_user.username = request.POST.get('loginUsername')
        auth_user.first_name = request.POST.get('name')
        auth_user.email = request.POST.get('emailLocal') + '@' + request.POST.get('emailDomain')
        user_profile.phone_number = request.POST.get('phone')
        user_profile.department = request.POST.get('department')
        user_profile.birth_date = request.POST.get('birth_date')
        user_profile.address_code = request.POST.get('addressCode')
        user_profile.address = request.POST.get('address')
        user_profile.address_detail = request.POST.get('addressDetail')
        user_profile.active_status = request.POST.get('active_status')
        user_profile.save()
        auth_user.save()
        return redirect("management:detail", id=id, flag=flag)

@csrf_exempt
def adminsignup(request):
    if request.method == 'GET':
        return render(request, 'management/adminsignup.html')
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
        
        user = User.objects.create_user(
            username = username,
            password = password,
            first_name = name,
            email = email,
            is_superuser = 1,
            is_active = 1
        )
        
        AdministratorProfile.objects.create(
            auth_user=user
            , birth_date=birth_date
            , phone_number=phone_number
            , address_code=address_code
            , address=address
            , address_detail=address_detail
            , department='관리자'
        )

        result = True
        msg = "회원가입 요청이 완료되었습니다."

        return JsonResponse({'result': result, 'msg': msg})

@csrf_exempt
def admincheck_username(request):
    username = request.POST.get('username')
    is_taken = User.objects.filter(username=username).exists()
    print(is_taken)
    return JsonResponse({'is_taken': is_taken})

def admincheck_email(request):
    email = request.GET.get('email')
    is_taken = User.objects.filter(email=email).exists()
    return JsonResponse({'is_taken': is_taken})

def admincheck_phone(request): 
    phone_number = request.GET.get('phone_number')
    is_taken = CounselorProfile.objects.filter(phone_number=phone_number).exists()
    return JsonResponse({'is_taken': is_taken})

def adminreset_password(request):
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
















def manager_edit(request, id):
    """
    개인정보 수정
    """
    user = get_object_or_404(CounselorProfile, id=id)
    data = {'user': user}
    #get으로 들어올시 기존값 반환
    if request.method == 'GET':
        return render(request, 'management/edit.html', data)
    #post로 들어올시 수정된값 반환
    else:
        print(user)
        user.name = request.POST.get('name') #이름
        # user.birthday = request.POST.get('birthday') #생년월일
        # user.phone_number = request.POST.get('phone_number') #전화번호
        user.username = request.POST.get('username') #id
        # user.password = request.POST.get('password') #pw
        user.email = request.POST.get('email') #이메일
        # user.address = request.POST.get('address') #주소
        # user.belong = request.POST.get('belong') # 소속
        # user.role = request.POST.get('role') #역할
        # user.active_status = request.POST.get('active_status') #활동상태
        user.save()
        return redirect("management:detail", id)




def approve_user(request, id):
    """
    가입 요청 승인
    """
    user = CounselorProfile.objects.get(id=id)
    data = CounselorProfile.objects.filter(active_status=0)
    user.active_status = 1
    user.save()
    return render(request, 'management/allow.html', {'data':data})


# 가입승인페이지
def allow(request):
    search_select = request.GET.get("searchSelect", "")
    search_text = request.GET.get("searchText", "")
    query = Q()

    if search_select:
        valid_fields = {
            'name': 'auth_user__first_name__icontains',
            'id': 'auth_user__username__icontains',
            'email': 'auth_user__email__icontains',
        }

        if search_select == 'all':
            for val in valid_fields.values():
                print(val)
                query |= Q(**{val: search_text})
        else:
            search_field = valid_fields[search_select]
            query = Q(**{search_field: search_text})

    data = CounselorProfile.objects.select_related('auth_user').filter(query)

    context = {
        'data': data,
        'searchSelect': search_select,
        'searchText': search_text,
    }

    return render(request, 'management/allow.html', context)


#활동중인 인원 구분 및 보류 위한 페이지
def inactive(request):
    search_select = request.GET.get("searchSelect", "")
    search_text = request.GET.get("searchText", "")
    query = Q()

    if search_select:
        valid_fields = {
            'name': 'auth_user__first_name__icontains',
            'id': 'auth_user__username__icontains',
            'email': 'auth_user__email__icontains',
        }

        if search_select == 'all':
            for val in valid_fields.values():
                print(val)
                query |= Q(**{val: search_text})
        else:
            search_field = valid_fields[search_select]
            query = Q(**{search_field: search_text})

    data = CounselorProfile.objects.select_related('auth_user').filter(query)

    context = {
        'data': data,
        'searchSelect': search_select,
        'searchText': search_text,
    }

    return render(request, 'management/inactive.html', context)


#비활성화 기능
def disable(request, id):
    user = get_object_or_404(CounselorProfile, id=id)
    data = CounselorProfile.objects.all()
    user.active_status = 0 
    user.save() 
    return render(request, 'management/detail.html', {'data':data}) 

#활성화 기능
def active(request, id):
    user = get_object_or_404(CounselorProfile, id=id)
    data = CounselorProfile.objects.all()
    user.active_status = 1  
    user.save() 
    return render(request, 'management/detail.html', {'data':data}) 


#휴직자 활성화기능
def leave_active(request, id):
    user = get_object_or_404(CounselorProfile, id=id)
    data = CounselorProfile.objects.all()
    user.active_status = 2  
    user.save() 
    return render(request, 'management/detail.html', {'data':data}) 

#퇴사자 활성화기능
def retire_active(request, id):
    user = get_object_or_404(CounselorProfile, id=id)
    data = CounselorProfile.objects.all()
    user.active_status = 3  
    user.save() 
    return render(request, 'management/detail.html', {'data':data})

# 보류자 활성화기능
def reject_active(request, id):
    user = get_object_or_404(CounselorProfile, id=id)
    data = CounselorProfile.objects.all()
    user.active_status = 4 
    user.save()
    return render(request, 'management/detail.html', {'data':data})

#테스트페이지
def test(request):
    data = CounselorProfile.objects.all()
    return render(request, 'management/test.html',{'data':data})

#검색로직
def search(request):
    query = request.POST.get('seachText', '')
   
    if query:
        results = CounselorProfile.objects.filter(name__icontains=query)
    else:
        results = []
    return render(request, 'management/dashboard.html', {'data': results, 'query': query})
       
def allow_search(request):
    query = request.POST.get('seachText', '')
    if query:
        results = CounselorProfile.objects.filter(name__icontains=query)
    else:
        results = []
    return render(request, 'management/manager_dashboard.html', {'': results, 'query': query})
         
def inactive_search(request):
    query = request.POST.get('seachText', '')
    if query:
        results = CounselorProfile.objects.filter(name__icontains=query)
    else:
        results = []
    return render(request, 'management/manager_dashboard.html', {'data': results, 'query': query})
