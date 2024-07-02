from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from chat import Chatbot
import os
import json
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from .models import EducationChatbotLog

def list(request):
    return render(request, 'education/index.html')

# 퀴즈페이지
def quiz(request):
    return render(request, 'education/quiz.html')

# 교육이력페이지
def edu_history(request):
    logs = EducationChatbotLog.objects.all()

    return render(request, 'education/edu_history.html', {'logs': logs})

# 교육이력 상세페이지
def details(request):
    return render(request, 'education/details.html')


# 웹에서 동작하는 Chatbot(미완성)
messages ="너는 친절하고 상냥하고 유능한 고객센터 상담원을 양성을 담당하는 교육자야. \
    교육을 위해 상담내역에서 자주 있거나 고객센터 매뉴얼을 참고해서 가상의 시뮬레이션을 진행할거야. \
    너가 고객이 되었다고 생각하고, 상담원에게 질문을 해줘"

chatbot = Chatbot(os.getenv("OPENAI_API_KEY"), 'database/chroma.sqlite3', messages) # chatbot 객체 생성


def chat_view(request):
    global chatbot
    if request.method == 'POST':
        print('request.POST:', request.POST)
        if 'category' in request.POST:
            # 카테고리 선택 및 챗봇 초기화
            category = request.POST.get('category')
            print("####################################")
            print('category:', category)
            print("####################################")

            api_key = os.environ['OPENAI_API_KEY']
            db_path = '../db'

            # Chatbot 객체 초기화
            behavior_policy = "너는 고객이고, 나는 상담사야. 너는 나에게 고객상담을 위한 질문을 해야해. 그에 대한 답변은 내가 할거야. 너는 나에게 '상담사님'이라고 해야해. 내가 답변할 수 있는 내용은 참고자료의 내용으로 답변할 수 있어."
            chatbot = Chatbot(api_key=api_key, db_path=db_path, behavior_policy=behavior_policy, category=category, THRESHOLD=2)

            # 첫 질문 생성
            initial_question = chatbot.chat("나에게 아무런 고객상담을 위한 질문을 해줄래?")

            return JsonResponse({'status': 'success', 'initial_question': initial_question})

        elif 'message' in request.POST:
            # 사용자 메시지 처리
            message = request.POST.get('message')
            print("####################################")
            print('Received message:', message)
            print("####################################")

            if chatbot is None:
                return JsonResponse({'response': 'Chatbot is not initialized. Please select a category first.'})

            # 사용자 메시지에 대한 응답 생성
            output = chatbot.chat(message)
            print("####################################")
            print('message:', message)
            print('output:', output)
            print("####################################")

            return JsonResponse({'response': output})

    return render(request, 'education/index.html')

def chat_view_test(request):
    global chatbot
    if request.method == 'POST':
        print('request.POST:', request.POST)
        if 'category' in request.POST:
            # 카테고리 선택 및 챗봇 초기화
            category = request.POST.get('category')
            print("####################################")
            print('category:', category)
            print("####################################")

            api_key = os.environ['OPENAI_API_KEY']
            db_path = '../db'

            # Chatbot 객체 초기화
            behavior_policy = "너는 고객이고, 나는 상담사야. 너는 나에게 고객상담을 위한 질문을 해야해. 그에 대한 답변은 내가 할거야. 너는 나에게 '상담사님'이라고 해야해. 내가 답변할 수 있는 내용은 참고자료의 내용으로 답변할 수 있어."
            chatbot = Chatbot(api_key=api_key, db_path=db_path, behavior_policy=behavior_policy, category=category, THRESHOLD=2)

            # 첫 질문 생성
            initial_question = chatbot.chat("나에게 아무런 고객상담을 위한 질문을 해줄래?")

            return JsonResponse({'status': 'success', 'initial_question': initial_question})

        elif 'message' in request.POST:
            # 사용자 메시지 처리
            message = request.POST.get('message')
            print("####################################")
            print('Received message:', message)
            print("####################################")

            if chatbot is None:
                return JsonResponse({'response': 'Chatbot is not initialized. Please select a category first.'})

            # 사용자 메시지에 대한 응답 생성
            output = chatbot.chat(message)
            print("####################################")
            print('message:', message)
            print('output:', output)
            print("####################################")

            return JsonResponse({'response': output})

    return render(request, 'education/chat.html')
