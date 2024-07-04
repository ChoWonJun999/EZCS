from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import User
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.db.models import Q

#관리자 메인페이지 DB에서 정보 받아오는 부분
def manager_dashboard(request):
    data = User.objects.all()
    return render(request, 'management/dashboard.html',{'data':data})

#상세페이지
def manager_detail(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'management/management_detail.html', {'user':user})

#개인정보 수정
def manager_edit(request, id):
    user = get_object_or_404(User, id=id)
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
        user.password = request.POST.get('password') #pw
        user.email = request.POST.get('email') #이메일
        # user.address = request.POST.get('address') #주소
        # user.belong = request.POST.get('belong') # 소속
        # user.role = request.POST.get('role') #역할
        # user.active_status = request.POST.get('active_status') #활동상태
        user.save()
        return redirect("management:management_detail", id)


# 가입승인페이지
def allow(request):
    data = User.objects.filter(active_status = 0)
    return render(request, 'management/allow.html',{'data':data})


#승인
def approve_user(request, id):
    user = User.objects.get(id=id)
    data = User.objects.filter(active_status = 0) 
    user.active_status = 1  
    user.save()  # 변경 사항 저장
    return render(request, 'management/allow.html',{'data':data}) 


#활동중인 인원 구분 및 보류 위한 페이지
def inactive(request):
    data = User.objects.filter(~Q(active_status = 0)) #여기서 사용하는 Q는 장고에서 쓰는 or
    return render(request, 'management/inactive.html', {'data':data})

#유저상세페이지
def detail(request, id):
    data = get_object_or_404(User, id=id)
    print(data.active_status)
    return render(request, 'management/detail.html', {'data':data}) 

#비활성화 기능
def disable(request, id):
    user = get_object_or_404(User, id=id)
    data = User.objects.all()
    user.active_status = 0 
    user.save() 
    return render(request, 'management/detail.html', {'data':data}) 

#활성화 기능
def active(request, id):
    user = get_object_or_404(User, id=id)
    data = User.objects.all()
    user.active_status = 1  
    user.save() 
    return render(request, 'management/detail.html', {'data':data}) 


#휴직자 활성화기능
def leave_active(request, id):
    user = get_object_or_404(User, id=id)
    data = User.objects.all()
    user.active_status = 2  
    user.save() 
    return render(request, 'management/detail.html', {'data':data}) 

#퇴사자 활성화기능
def retire_active(request, id):
    user = get_object_or_404(User, id=id)
    data = User.objects.all()
    user.active_status = 3  
    user.save() 
    return render(request, 'management/detail.html', {'data':data})

# 보류자 활성화기능
def reject_active(request, id):
    user = get_object_or_404(User, id=id)
    data = User.objects.all()
    user.active_status = 4 
    user.save()
    return render(request, 'management/detail.html', {'data':data})

def test(request):
    data = User.objects.all()
    return render(request, 'management/test.html',{'data':data})


def search(request):
    query = request.POST.get('seachText', '')
    if query:
        results = User.objects.filter(name__icontains=query)
    else:
        results = User.objects.all()
    return render(request, 'management/test.html', {'data': results, 'query': query})

         
