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

# 가입요청유저상세페이지
def allow_detail(request, id):
    user = get_object_or_404(User, id=id)
    print(user)
    return render(request, 'management/allow_detail.html', {'user':user})   


#승인
def approve_user(request, id):
    if request.method == 'POST':
        selected_id= request.POST.getlist('selected_items')
        users = User.objects.filter(id__in=selected_id)
        for user in users:  # 각 사용자에 대해 반복
            user.active_status = 1  
            user.save()  # 변경 사항 저장
            user.save()
        return redirect('management:allow')
    return render(request, 'management/allow.html') 

#비활성화 페이지 다시 활성화 시킬때 
def inactive_active(request, id):
    if request.method == 'POST':  # 요청 메서드가 POST인지 확인
        selected_items = request.POST.getlist('selected_items')  # POST 데이터에서 선택된 항목의 ID 리스트 가져오기
        print(selected_items)
        users = User.objects.filter(id__in=selected_items)
        for user in users:  # 각 사용자에 대해 반복
            user.active_status = 1  
            user.save()  # 변경 사항 저장
        return redirect('management:inactive')  # 처리 완료 후 사용자 리스트 페이지로 리다이렉트
    return render(request, 'management/inactive.html')   
    

#퇴사 페이지 다시 활성화 시킬때
def retire_active(request, id):
    if request.method == 'POST':  # 요청 메서드가 POST인지 확인
        selected_items = request.POST.getlist('selected_items')  # POST 데이터에서 선택된 항목의 ID 리스트 가져오기
        print(selected_items)
        users = User.objects.filter(id__in=selected_items)
        for user in users:  # 각 사용자에 대해 반복
            user.active_status = 1  
            user.save()  # 변경 사항 저장
        return redirect('management:retire')  # 처리 완료 후 사용자 리스트 페이지로 리다이렉트
    return render(request, 'management/retire.html')
    

#휴직 페이지 다시 활성화 시킬때
def leave_active(request, id):
    if request.method == 'POST':  # 요청 메서드가 POST인지 확인
        selected_items = request.POST.getlist('selected_items')  # POST 데이터에서 선택된 항목의 ID 리스트 가져오기
        print(selected_items)
        users = User.objects.filter(id__in=selected_items)
        for user in users:  # 각 사용자에 대해 반복
            user.active_status = 1  
            user.save()  # 변경 사항 저장
        return redirect('management:leave')  # 처리 완료 후 사용자 리스트 페이지로 리다이렉트
    return render(request, 'management/leave.html') 

#보류 페이지 다시 활성화 시킬때
def reject_active(request, id):
    if request.method == 'POST':  # 요청 메서드가 POST인지 확인
        selected_items = request.POST.getlist('selected_items')  # POST 데이터에서 선택된 항목의 ID 리스트 가져오기
        print(selected_items)
        users = User.objects.filter(id__in=selected_items)
        for user in users:  # 각 사용자에 대해 반복
            user.active_status = 1  
            user.save()  # 변경 사항 저장
        return redirect('management:reject')  # 처리 완료 후 사용자 리스트 페이지로 리다이렉트
    return render(request, 'management/reject.html') 


#활동중인 인원 구분 및 보류 위한 페이지
def inactive(request):
    data = User.objects.filter(~Q(active_status = 0)) #여기서 사용하는 Q는 장고에서 쓰는 or
    return render(request, 'management/inactive.html', {'data':data})

#유저상세페이지
def detail(request, id):
    data = get_object_or_404(User, id=id)
    print(data.active_status)
    return render(request, 'management/detail.html', {'data':data})   

#퇴사자 페이지
def retire(request):
    data = User.objects.filter(Q(active_status = 3)) #여기서 사용하는 Q는 장고에서 쓰는 or
    return render(request, 'management/retire.html', {'data':data})
#퇴사자 상세 페이지
def retire_detail(request, id):
    data = get_object_or_404(User, id=id)
    print(data.active_status)
    return render(request, 'management/retire_detail.html', {'data':data})

#휴직자 페이지
def leave(request):
    data = User.objects.filter(Q(active_status = 2)) #여기서 사용하는 Q는 장고에서 쓰는 or
    return render(request, 'management/retire.html', {'data':data})

#휴직자 상세페이지
def leave_detail(request, id):
    data = get_object_or_404(User, id=id)
    print(data.active_status)
    return render(request, 'management/retire_detail.html', {'data':data})

#보류 페이지
def reject(request):
    data = User.objects.filter(Q(active_status = 4)) #여기서 사용하는 Q는 장고에서 쓰는 or
    return render(request, 'management/reject.html', {'data':data})

#보류자 상세페이지
def reject_detail(request, id):
    data = get_object_or_404(User, id=id)
    print(data.active_status)
    return render(request, 'management/retire_detail.html', {'data':data})

#검색 로직
def search(request):
    query = request.GET.get('query')
    if query:
        results = User.objects.filter(name__icontains=query)
    else:
        results = []
    
    print('='*30)
    print(query)
    print('='*30)
    return render(request, 'management/manager_dashboard.html', {'results': results, 'query': query})
#일괄선택해서 데이터 처리하는 기능
# def all(request):
#     if request.method == 'POST':  # 요청 메서드가 POST인지 확인
#         selected_items = request.POST.getlist('selected_items')  # POST 데이터에서 선택된 항목의 ID 리스트 가져오기
#         print(selected_items)
#         users = User.objects.filter(id__in=selected_items)
#         for user in users:  # 각 사용자에 대해 반복
#             user.active_status = 1  
#             user.save()  # 변경 사항 저장
#         return redirect('management:reject')  # 처리 완료 후 사용자 리스트 페이지로 리다이렉트
#     return render(request, 'management/reject.html')  
         