from django.shortcuts import render
from django.http import JsonResponse
import os
from stt import STTModel
from chat import Chatbot
from django.views.decorators.csrf import csrf_exempt
import logging

def list(request):
    return render(request, 'counseling/index.html')


stt_model = STTModel(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
)

logger = logging.getLogger(__name__)

@csrf_exempt
def stt(request):
    logger.info("#########################")
    logger.info('stt request: %s', request)
    logger.info("#########################")
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        
        # 음성 데이터를 파일로 저장하지 않고 메모리에서 바로 읽습니다.
        audio_data = audio_file.read()

        text = stt_model.request(audio_data)

        return JsonResponse({'text': text})

    return JsonResponse({'error': 'Invalid request'}, status=400)



messages ="너는 친절하고 상냥하고 유능한 고객센터 상담원이야. \
    고객의 질문에 대해 상담내역에서 자주 있거나 고객센터 매뉴얼을 참고해서 완벽한 답변을 해줘."
    
chatbot = Chatbot(os.getenv("OPENAI_API_KEY"), 'database/chroma.sqlite3', messages) # chatbot 객체 생성


def stt_chat(request):
    print("#########################")
    print('request', request)
    print("#########################")
    
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        
        # 음성 데이터를 파일로 저장하지 않고 메모리에서 바로 읽습니다.
        audio_data = audio_file.read()

        text = stt_model.request(audio_data)
        print("#########################")
        print('text', text)
        print("#########################")

        output = chatbot.chat(text)

        return JsonResponse({
            'text': text,
            'output': output
            })

    return JsonResponse({'error': 'Invalid request'}, status=400)
