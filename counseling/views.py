from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import os
from stt import STTModel
from chat import Chatbot
from django.views.decorators.csrf import csrf_exempt
import logging
from .models import *
import json
from django.http import HttpResponse
import random
# def list(request):
#     data = CustomerInfo.objects.get(phone_number='01011112222')
#     print(data)
#     return render(request, "counseling/index.html",{'data':data})

def list(request):
    customer_info_queryset = CustomerInfo.objects.all()

    if customer_info_queryset.exists():
        # 랜덤으로 고객 정보 중 하나를 선택
        random_customer = random.choice(customer_info_queryset)
        # 선택된 고객의 상담 기록을 모두 가져오기
        counsel_logs_queryset = CounselLog.objects.filter(phone_number=random_customer.phone_number)

        if counsel_logs_queryset.exists():
            # 랜덤으로 상담 기록 중 하나를 선택
            random_counsel_log = random.choice(counsel_logs_queryset)

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
                'customer_info': [random_customer],  # 리스트로 전달
                'counsel_logs': [random_counsel_log]  # 리스트로 전달
            }
        else:
            # 상담 기록이 없는 경우 빈 리스트 전달
            context = {
                'customer_info': [random_customer],  # 리스트로 전달
                'counsel_logs': []
            }
    else:
        # 고객 정보가 없는 경우 빈 리스트 전달
        context = {
            'customer_info': [],
            'counsel_logs': []
        }

    return render(request, "counseling/index.html", context)
# 상담이력 뷰
def history(request):
    query = request.POST.get('searchText', '')

    if query:
        logs = CounselLog.objects.filter(body__icontains=query)
    else:
        logs = CounselLog.objects.all()

    return render(request, 'counseling/history.html', {'logs': logs})


stt_model = STTModel(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
)

logger = logging.getLogger(__name__)


@csrf_exempt
def stt(request):
    logger.info("#########################")
    logger.info("stt request: %s", request)
    logger.info("#########################")
    if request.method == "POST" and request.FILES.get("audio"):
        audio_file = request.FILES["audio"]

        # 음성 데이터를 파일로 저장하지 않고 메모리에서 바로 읽습니다.
        audio_data = audio_file.read()

        text = stt_model.request(audio_data)

        return JsonResponse({"text": text})

    return JsonResponse({"error": "Invalid request"}, status=400)


messages = "너는 친절하고 상냥하고 유능한 고객센터 상담원이야. \
      고객의 질문에 대해 고객센터 매뉴얼을 참고해서 완벽한 답변 대본을 작성해줘.\
      예시: 네, 고객님 해당 문의 내용은 월사용요금을 kt에서 신용카드사로 청구하면 고객이 신용카드사에 결제대금을 납부하는 제도입니다."


chatbot = Chatbot(
    os.getenv("OPENAI_API_KEY"), "database/chroma.sqlite3", behavior_policy=messages
)  # chatbot 객체 생성


# def stt_chat(request):
#     print("#########################")
#     print('request', request)
#     print("#########################")

#     if request.method == 'POST' and request.FILES.get('audio'):
#         audio_file = request.FILES['audio']

#         # 음성 데이터를 파일로 저장하지 않고 메모리에서 바로 읽습니다.
#         audio_data = audio_file.read()

#         text = stt_model.request(audio_data)
#         print("#########################")
#         print('text', text)
#         print("#########################")

#         output = chatbot.chat(text)

#         return JsonResponse({
#             'text': text,
#             'output': output
#             })

#     return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def stt_chat(request):
    if request.method == "POST":
        text = request.POST.get("text")

        if text:
            output = chatbot.chat(text)
            return JsonResponse({"text": text, "output": output})

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def save_customer_info(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer-name")
        birth_date = request.POST.get("birthdate")
        phone_number = request.POST.get("phone")
        address = request.POST.get("address")
        joined_date = request.POST.get("join-date")

        print(customer_name)
        print(birth_date)
        print(phone_number)
        print(address)
        print(joined_date)

        try:
            customer_info = CustomerInfo(
                phone_number=phone_number,
                name=customer_name,
                birth_date=birth_date,
                joined_date=joined_date,
                address=address,
            )
            customer_info.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def save_counseling_log(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            
            username = data.get("username")
            phone_number_str = data.get("phone_number")

            try:
                phone_number = CustomerInfo.objects.get(phone_number=phone_number_str)
            except CustomerInfo.DoesNotExist:
                return JsonResponse({"success": False, "error": "CustomerInfo not found"})

            chat_data = json.dumps(data.get("chat_data", {}), ensure_ascii=False)
            memo_data = json.dumps(data.get("memo_data", {}), ensure_ascii=False)
            
            print(f"Username: {username}")
            print(f"Phone Number: {phone_number}")
            print(f"Chat Data: {chat_data}")
            print(f"Memo Data: {memo_data}")

            counselLog = CounselLog(
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
                counsel_log = CounselLog.objects.get(id=log_id)
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
def evaluation_chat(request):
    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            output = chatbot.chat(text)
            return JsonResponse({"text": text, "output": output})
    return JsonResponse({"error": "Invalid request"}, status=400)