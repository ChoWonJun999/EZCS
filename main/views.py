from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

def user_dashboard(request):
    return render(request, 'main/index.html')

def start_ezcs(request):
    return render(request, 'startezcs.html')

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.birth_date = request.POST.get('birth_date')
        user.address_code = request.POST.get('address_code')
        user.address = request.POST.get('address')
        user.address_detail = request.POST.get('address_detail')

        password = request.POST.get('password')
        if password:
            try:
                validate_password(password, user)
                user.password = make_password(password)
            except ValidationError:
                return JsonResponse({'result': False, 'msg': '비밀번호가 유효하지 않습니다.'})

        user.save()
        return JsonResponse({'result': True, 'msg': '회원정보가 성공적으로 수정되었습니다.'})

    return render(request, 'main/edit_profile.html', {'user': user})

def contract(request):
    return render(request, 'main/contract.html')

def privacy(request):
    return render(request, 'main/privacy.html')