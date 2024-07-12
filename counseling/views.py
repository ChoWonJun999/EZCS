from django.shortcuts import render
from django.http import JsonResponse
from chat import Chatbot
from django.views.decorators.csrf import csrf_exempt
import logging
from .models import *
from django.db.models import Q
import json
from django.core.paginator import Paginator
from django.http import HttpResponse
import random


logger = logging.getLogger(__name__)


def counsel(request):
    """
    상담 페이지
    """
    customer = CustomerProfile.objects.order_by('?').first()

    if customer:
        # 선택된 고객의 상담 기록을 모두 가져오기
        log = Log.objects.filter(customer=customer)

        if log:
            # 랜덤으로 상담 기록 중 하나를 선택
            random_counsel_log = random.choice(log)

            try:
                if isinstance(random_counsel_log.memo, str):
                    memo_json = json.loads(random_counsel_log.memo)  # memo 필드를 JSON 형식으로 파싱
                elif isinstance(random_counsel_log.memo, dict):
                    memo_json = random_counsel_log.memo
                else:
                    memo_json = {}
                random_counsel_log.inquiry_text = memo_json.get('inquiry_text', '')
                random_counsel_log.action_text = memo_json.get('action_text', '')
            except (TypeError, json.JSONDecodeError) as e:
                print(f"Error parsing memo for log {random_counsel_log.id}: {e}")
                random_counsel_log.inquiry_text = ''
                random_counsel_log.action_text = ''

            context = {
                'customer': customer
                , 'counsel_logs': [random_counsel_log]  # 리스트로 전달
            }
        else:
            # 상담 기록이 없는 경우 빈 리스트 전달
            context = {
                'customer': customer
                , 'counsel_logs': []
            }
    else:
        # 고객 정보가 없는 경우 빈 리스트 전달
        context = {
            'customer_info': None,
            'counsel_logs': []
        }

    return render(request, "counseling/index.html", context)


def save_customer_info(request):
    """
    고객 정보 수정
    """
    if request.method == "POST":
        customer_id = request.POST.get("customer-id")
        customer_name = request.POST.get("customer-name")
        birth_date = request.POST.get("birthdate")
        phone_number = request.POST.get("phone")
        address = request.POST.get("address")
        joined_date = request.POST.get("join-date")

        print(customer_id)
        print(customer_name)
        print(birth_date)
        print(phone_number)
        print(address)
        print(joined_date)

        try:
            customer = CustomerProfile.objects.get(id=customer_id)
            # Update the attributes
            customer.phone_number = phone_number
            customer.customer_name = customer_name
            customer.birth_date = birth_date
            customer.joined_date = joined_date
            customer.address = address
            customer.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"error": "Invalid request"}, status=400)








# 상담이력 뷰
def history(request):
    query = request.POST.get('searchText', '')

    if query:
        logs = Log.objects.filter(body__icontains=query)
    else:
        logs = Log.objects.all()

    # 검색 필터링 처리
    search_text = request.GET.get("searchText", "")
    category = request.GET.get("category", "")
    result = request.GET.get("result", "")

    if search_text:
        logs = logs.filter(
            Q(user_id__username__icontains=search_text)
            | Q(user_id__name__icontains=search_text)
        )

    if category:
        logs = logs.filter(category=category)

    if result:
        if result == "pass":
            logs = logs.filter(is_passed=True)
        elif result == "fail":
            logs = logs.filter(is_passed=False)

    # 페이지네이션 처리
    paginator = Paginator(logs, 10)  # 페이지당 10개씩 표시
    page = request.GET.get("page")
    logs = paginator.get_page(page)

    return render(
        request,
        "counseling/history.html",
        {"logs": logs, "is_paginated": logs.has_other_pages()},
    )

@csrf_exempt
def save_counseling_log(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            
            username = data.get("username")
            phone_number_str = data.get("phone_number")

            try:
                phone_number = CustomerProfile.objects.get(phone_number=phone_number_str)
            except CustomerProfile.DoesNotExist:
                return JsonResponse({"success": False, "error": "CustomerProfile not found"})

            chat_data = json.dumps(data.get("chat_data", {}), ensure_ascii=False)
            memo_data = json.dumps(data.get("memo_data", {}), ensure_ascii=False)
            
            print(f"Username: {username}")
            print(f"Phone Number: {phone_number}")
            print(f"Chat Data: {chat_data}")
            print(f"Memo Data: {memo_data}")

            counselLog = Log(
                username=username,
                phone_number=phone_number,
                body=chat_data,
                memo=memo_data,
            )
            counselLog.save()

            return JsonResponse({"success": True})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def save_consultation(request):
    if request.method == 'POST':
        try:
            log_id = request.POST.get('log_id')
            inquiry_text = request.POST.get('inquiry_text')
            action_text = request.POST.get('action_text')

            if log_id and (inquiry_text or action_text):
                counsel_log = Log.objects.get(id=log_id)
                memo = json.loads(counsel_log.memo) if isinstance(counsel_log.memo, str) else counsel_log.memo or {}
                memo['inquiry_text'] = inquiry_text
                memo['action_text'] = action_text
                counsel_log.memo = json.dumps(memo, ensure_ascii=False)
                counsel_log.save()

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Missing log_id, inquiry_text, or action_text'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def save_consultation(request):
    if request.method == 'POST':
        try:
            log_id = request.POST.get('log_id')
            inquiry_text = request.POST.get('inquiry_text')
            action_text = request.POST.get('action_text')

            if log_id and (inquiry_text or action_text):
                counsel_log = Log.objects.get(id=log_id)
                memo = json.loads(counsel_log.memo) if isinstance(counsel_log.memo, str) else counsel_log.memo or {}
                memo['inquiry_text'] = inquiry_text
                memo['action_text'] = action_text
                counsel_log.memo = json.dumps(memo, ensure_ascii=False)
                counsel_log.save()

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Missing log_id, inquiry_text, or action_text'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})