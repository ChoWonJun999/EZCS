from django.shortcuts import render
from django.http import JsonResponse
import os
from stt import STTModel
from chat import Chatbot
from django.views.decorators.csrf import csrf_exempt
import logging
from .models import CounselLog, CustomerInfo, User


def list(request):
    data = CustomerInfo.objects.get(phone_number='01011112222')
    print(data)
    return render(request, "counseling/index.html",{'data':data})



def test(request):
    return render(request, "counseling/test.html")


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


chatbot = Chatbot(os.getenv("OPENAI_API_KEY"), "database/chroma.sqlite3", behavior_policy=messages)  # chatbot 객체 생성


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
    print("#########################")
    print("request", request)
    print("#########################")

    if request.method == "POST":
        text = request.POST.get("text")
        print(text)


        if text:
                print("#########################")
                print("text", text)
                print("username", username)
                print("phone_number", phone_number)
                print("#########################")

                output = chatbot.chat(text)
                # customer_info = CustomerInfo.objects.get(phone_number=phone_number)
                # print(customer_info)
                
                # counselLog_instance = CounselLog(
                #     username=username,
                #     body={"prompt": text, "output": output},
                #     phone_number=customer_info,
                # )
                # counselLog_instance.save()

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
