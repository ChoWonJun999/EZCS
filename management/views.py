from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import User
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.db.models import Q

#관리자 메인페이지 DB에서 정보 받아오는 부분
def manager_dashboard(request):
    data = User.objects.all()
    return render(request, 'management/manager_dashboard.html',{'data':data})

#상세페이지
def manager_detail(request, id):
    user = User.objects.get(id=id)
    return render(request, 'management/management_detail.html', {'user':user})

#개인정보 수정
def manager_edit(request, id):
    print('='*100)
    print(request.method)
    print('='*100)
    user = get_object_or_404(User, id=id)
    data = {'user': user}
    #get으로 들어올시 기존값 반환
    if request.method == 'GET':
        return render(request, 'management/management_edit.html', data)
    #post로 들어올시 수정된값 반환
    else:
        user.username = request.POST.get('username')
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.save()
        return redirect("management:management_detail", id)

# 가입승인페이지
def allow(request):
    data = User.objects.filter(active_status = 0)
    return render(request, 'management/allow.html',{'data':data})

# def allow_detail(request, id):
#     user = User.objects.get(id=id)
#     return render(request, 'management/management_detail.html', {'user':user})   

#승인
def approve_user(request, id):
    user = get_object_or_404(User, id=id)
    print('hi')
    print(user.active_status)
    user.active_status = 1
    user.save()
    return redirect('management:allow')


#거부
# def reject_user(request, id):
#     user = get_object_or_404(User, id=id)
#     user.active_status = 4
#     user.save()
#     return render(request, 'management/allow.html',{'user':user})


#퇴사자 및 휴직자 페이지
def quitter(request):
    data = User.objects.filter(Q(active_status = 2) | Q(active_status = 3)) #여기서 사용하는 Q는 장고에서 쓰는 or
    return render(request, 'management/quitter.html', {'data':data})