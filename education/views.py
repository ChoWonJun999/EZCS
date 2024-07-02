from django.shortcuts import render
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from chat import Chatbot
import os

# 웹에서 동작하는 Chatbot(미완성)
messages ="너는 친절하고 상냥하고 유능한 고객센터 상담원을 양성을 담당하는 교육자야. \
    교육을 위해 상담내역에서 자주 있거나 고객센터 매뉴얼을 참고해서 가상의 시뮬레이션을 진행할거야. \
    너가 고객이 되었다고 생각하고, 상담원에게 질문을 해줘"

chatbot = Chatbot(os.getenv("OPENAI_API_KEY"), 'database/chroma.sqlite3', messages) # chatbot 객체 생성

class ChatbotView(View):
    """
    Chatbot Response
    """
    def get(self, request):
        return render(request, 'chatbot/chat.html')

    def post(self, request):
        user_input = request.POST.get('user_input')
        if user_input:
            response = chatbot.chat(user_input)
            return JsonResponse({'response': response})
        return JsonResponse({'error': 'Invalid input'}, status=400)

def list(request):
    return render(request, 'education/index.html')

# 퀴즈페이지
def quiz(request):
    return render(request, 'education/quiz.html')

# 교육이력페이지
def edu_history(request):
    return render(request, 'education/edu_history.html')

# 교육이력 상세페이지
def details(request):
    return render(request, 'education/details.html')