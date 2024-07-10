from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import CounselorProfile
from django.db.models import Q


def dashboard(request):
    """
    관리자 메인페이지 DB에서 정보 받아오는 부분
    """
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

    return render(request, 'management/dashboard.html', context)


#유저상세페이지
def detail(request, id):
    data = get_object_or_404(CounselorProfile.objects.select_related('auth_user'), id=id)
    return render(request, 'management/detail.html', {'data':data}) 


#개인정보 수정
def manager_edit(request, id):
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


#승인
def approve_user(request, id):
    user = CounselorProfile.objects.get(id=id)
    data = CounselorProfile.objects.filter(active_status = 0) 
    user.active_status = 1  
    user.save()  # 변경 사항 저장
    return render(request, 'management/allow.html',{'data':data}) 



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
         