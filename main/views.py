from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import User, CounselorProfile  
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from management.models import Board
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from counseling.models import Log as CounselLog
from education.models import Log as EducationLog, QuizHistory
from django.db.models import Count, DateField
from django.db.models.functions import Cast


def user_dashboard(request):
    notices = Board.objects.filter(flag=0).order_by('-create_time')
    paginator = Paginator(notices, 10)
    page = request.GET.get('page')
    notices = paginator.get_page(page)
    return render(request, 'main/index.html', {'notices': notices})


def get_log_data(model_class, start, end, request_user_id=None):
    queryset = model_class.objects.filter(create_time__gte=start, create_time__lte=end)\
        .annotate(date=Cast('create_time', output_field=DateField()))\
            .values('date')\
                .annotate(count=Count('id'))\
                    .order_by('date')
    
    if request_user_id is not None:
        queryset = queryset.filter(auth_user=request_user_id)
    
    return [{'type': str(model_class), 'date': item['date'], 'count': item['count']} for item in queryset]


def get_calendar(request, start, end):
    start += " 00:00:00"
    end += " 00:00:00"

    if request.user.is_superuser:
        counsel_data = get_log_data(CounselLog, start, end)
        education_data = get_log_data(EducationLog, start, end)
        quiz_data = get_log_data(QuizHistory, start, end)
    else:
        counsel_data = get_log_data(CounselLog, start, end, request.user.id)
        education_data = get_log_data(EducationLog, start, end, request.user.id)
        quiz_data = get_log_data(QuizHistory, start, end, request.user.id)
    
    data = counsel_data + education_data + quiz_data

    return JsonResponse(data, safe=False)


def notice_detail(request, id):
    notice = get_object_or_404(Board, id=id)
    is_image = False
    if notice.file:
        is_image = notice.file.url.lower().endswith(('.jpg', '.jpeg', '.png'))
    return render(request, 'main/notice_detail.html', {'notice': notice, 'is_image': is_image})


def start_ezcs(request):
    return render(request, 'main/startezcs.html')


def edit_profile(request):
    if not request.session.get('password_verified'):
        return redirect('main:user_dashboard')  # 비밀번호 확인 안된 경우 대시보드로 리다이렉트

    user = request.user
    profile = get_object_or_404(CounselorProfile, auth_user=user)  # 수정된 부분
    email_local, email_domain = user.email.split('@')


    if request.method == 'POST':
        user.first_name = request.POST.get('name')
        user.email = request.POST.get('email') 

        profile.phone_number = request.POST.get('phone_number')
        profile.birth_date = request.POST.get('birth_date')
        profile.address_code = request.POST.get('address_code')
        profile.address = request.POST.get('address')
        profile.address_detail = request.POST.get('address_detail')
        password = request.POST.get('password')
        if password:
            try:
                validate_password(password, user)
                user.password = make_password(password)
            except ValidationError as e:
                return JsonResponse({'result': False, 'msg': '비밀번호가 유효하지 않습니다. ' + ' '.join(e.messages)})

        user.save()
        profile.save()  
        request.session['password_verified'] = False  # 수정 후 세션 상태 초기화

        return JsonResponse({'result': True, 'msg': '회원정보가 성공적으로 수정되었습니다.'})
    email_domains = ["naver.com", "gmail.com", "daum.net", "nate.com"]

    return render(request, 'main/edit_profile.html', {
        'user': user,
        'profile': profile,
        'email_local': email_local,
        'email_domain': email_domain,
        'email_domains': email_domains
    })

def contract(request):
    return render(request, 'main/contract.html')


def privacy(request):
    return render(request, 'main/privacy.html')


@csrf_exempt
def verify_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = request.user
        authenticated_user = authenticate(username=user.username, password=password)

        if authenticated_user is not None:
            request.session['password_verified'] = True
            return JsonResponse({'valid': True})
        else:
            return JsonResponse({'valid': False})

    return JsonResponse({'valid': False})