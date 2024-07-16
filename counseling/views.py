from django.shortcuts import render
from django.http import JsonResponse
from chat import Chatbot
from chat_trans import Chatbot_trans
from django.views.decorators.csrf import csrf_exempt
import logging
from .models import *
from django.db.models import Q
import json
from django.core.paginator import Paginator
import random
from django.conf import settings
from datetime import datetime, timedelta
from abuse_filter import AbuseFilter


logger = logging.getLogger(__name__)
abuse_filter = AbuseFilter()

trans_chat_bot = None
recommend_chat_bot = None 

def counsel(request):
    """
    상담 페이지
    """
    if request.method == 'POST':
        global trans_chat_bot, recommend_chat_bot
        id = request.POST.get('customerId')
        customer = CustomerProfile.objects.get(id=id)
        log = Log.objects.create(
            auth_user_id = request.user.id
            , customer_id = id
        )
        context = {
            'logId': log.id
            , 'customer': customer
        }
        trans_chat_bot = Chatbot_trans(
            model_id='ft:gpt-3.5-turbo-0125:personal::9god26fK',
            behavior_policy='방언을 표준어로 번역해주세요.'
        )
        
        messages = "너는 친절하고 상냥하고 유능한 고객센터 상담원이야. \
        고객의 질문에 대해 고객센터 매뉴얼을 참고해서 완벽한 답변 대본을 작성해줘.\
        예시: 네, 고객님 해당 문의 내용은 월사용요금을 kt에서 신용카드사로 청구하면 고객이 신용카드사에 결제대금을 납부하는 제도입니다."

        recommend_chat_bot = Chatbot(
            behavior_policy=messages,
            k = 1
        )
        
        return render(request, "counseling/index.html", context)
    
    customer = CustomerProfile.objects.order_by('?').first()
    context = {'customer': customer}
    return render(request, "counseling/index.html", context)


def update_log(request):
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
        log_id = request.POST.get("logId")
        inquiries = request.POST.get("inquiries")
        action = request.POST.get("action")

        try:
            customer = CustomerProfile.objects.get(id=customer_id)
            customer.phone_number = phone_number
            customer.customer_name = customer_name
            customer.birth_date = birth_date
            customer.joined_date = joined_date
            customer.address = address
            customer.save()
            log = Log.objects.get(id=log_id)
            log.inquiries = inquiries
            log.action = action
            log.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"error": "Invalid request"}, status=400)


def ai_model(request):
    if request.method == "POST":
        classify = request.POST.get("classify")
        message = request.POST.get("message")
        log_id = request.POST.get("logId")
        try:
            classify = 0 if classify == 'customer' else 1
            columns = {
                "classify": classify
                , "message": message
                , "log_id": log_id
            }
            result = {
                "success": True
            }
            if not classify:
                global trans_chat_bot, recommend_chat_bot
                trans_output = trans_chat_bot.ask(message)
                trans_output = abuse_filter.abuse_clean(trans_output)
                recommend_output = recommend_chat_bot.chat(message)
                columns['recommend'] = recommend_output
                columns['translate'] = trans_output
                result['recommend_output'] = recommend_output
                result['trans_output'] = trans_output

            LogItem.objects.create(**columns)
            
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"error": "Invalid request"}, status=400)


def history(request):
    """
    상담 이력 페이지
    """
    search_text = request.GET.get("searchText", "")
    search_select = request.GET.get("searchSelect", "")
    
    start_date = request.GET.get("startDate", "")
    end_date = request.GET.get("endDate", "")

    query = Q()
    if not request.user.is_superuser:
        query = Q(auth_user=request.user.id)
    
    query1 = Q()
    if search_text:
        query1 = Q(customer__name__icontains=search_text)

    query2 = Q()
    if start_date and end_date:
        query2 &= Q(create_time__gte=start_date)
        query2 &= Q(create_time__lte=end_date)
    else:
        one_month_ago = datetime.now() - timedelta(days=30)
        query2 &= Q(create_time__gte=one_month_ago)
        query2 &= Q(create_time__lte=datetime.now())
        start_date = one_month_ago.strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

    data = Log.objects.filter(query & query1 & query2).order_by('-create_time', 'customer_id', 'auth_user_id')

    paginator = Paginator(data, 10)
    page = request.GET.get('page')
    data = paginator.get_page(page)

    context = {
        'data': data,
        'searchSelect': search_select,
        'searchText': search_text,
        'startDate': start_date,
        'endDate': end_date,
        'is_paginated': data.has_other_pages(),
    }
    return render(request, "counseling/history.html", context)

def detail(request, id):
    head = Log.objects.get(id=id)
    data = LogItem.objects.filter(log_id=id)
    context = {
        'head': head
        , 'data': data
    }
    return render(request, "counseling/detail.html", context)
















def list(request):
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