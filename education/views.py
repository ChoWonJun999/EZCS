import json
import random
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import QuizForm
from chat import Chatbot
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator  # Paginator 임포트
from django.db.models import Q

# 교육
def list(request):
    return render(request, 'education/index.html')

# 교육 이력
def edu_history(request):
    logs = EducationChatbotLog.objects.all()

    # 검색 기능을 추가합니다.
    search_text = request.GET.get('searchText', '')
    category = request.GET.get('category', '')

    if search_text:
        logs = logs.filter(body__icontains=search_text)
    if category:
        logs = logs.filter(body__icontains=category)

    # 페이지네이션
    paginator = Paginator(logs, 10)  # 페이지당 10개씩 표시
    page_number = request.GET.get('page')
    logs_page = paginator.get_page(page_number)

    return render(request, 'education/edu_history.html', {'logs': logs_page})


# 교육 이력 상세
def edu_detail(request, log_id):
    log = get_object_or_404(EducationChatbotLog, id=log_id)
    return render(request, 'education/edu_details.html', {'log': log})

# 롤플레잉 저장 함수 - 미완성
@csrf_exempt
def save_chat_data(request):
    if request.method == 'POST':
        user = request.user
        category = request.POST.get('category')
        chat = request.POST.get('chat')

        body = {
            "category": category,
            "chat": chat
        }

        EducationChatbotLog.objects.create(
            user_id=user,
            body=body
        )

        return JsonResponse({"message": "Data saved successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)

# 퀴즈페이지
@csrf_exempt
@login_required
def quiz(request):
    quizzes = Quiz.objects.order_by('?')[:5]  # 퀴즈 5개를 랜덤으로 가져오기

    if request.method == 'POST':  # 폼 제출이 POST 요청으로 이루어질 때
        form = QuizForm(request.POST)
        if form.is_valid():
            answers = json.loads(form.cleaned_data['answers'])
            quiz_ids = [int(id) for id in json.loads(form.cleaned_data['quiz_ids'])]

            # 디버깅 정보 출력
            print(f'answers: {answers}')
            print(f'quiz_ids: {quiz_ids}')

            results = {}
            correct_answers = 0  # 정답 개수를 세기 위한 변수 초기화

            for idx, answer in enumerate(answers):  # 제출된 답변들을 순회하면서
                try:
                    quiz = Quiz.objects.get(id=quiz_ids[idx])  # 현재 퀴즈 ID로 퀴즈 객체 가져오기
                except Quiz.DoesNotExist:
                    # 퀴즈가 존재하지 않을 경우 오류 출력
                    print(f'Quiz with id {quiz_ids[idx]} does not exist.')
                    continue

                is_correct = False  # 초기 값은 오답으로 설정
                if quiz.flag == 0 and quiz.answer.strip().lower() == answer.strip().lower():  # 단답형 퀴즈의 경우
                    is_correct = True  # 정답일 경우
                    correct_answers += 1  # 정답 개수 증가
                elif quiz.flag == 1 and str(quiz.answer) == answer:  # 객관식 퀴즈의 경우
                    is_correct = True  # 정답일 경우
                    correct_answers += 1  # 정답 개수 증가
                
                results[quiz.id] = {  # 결과 딕셔너리에 현재 퀴즈의 정답 여부와 사용자의 답변 저장
                    'is_correct': is_correct,
                    'user_answer': answer,
                    'commentary': quiz.commentary,  # 해설 추가
                    'correct_answer': quiz.answer
                }

            is_passed = correct_answers >= 3  # 3개 이상의 정답이면 통과로 설정
            categories = [Quiz.objects.get(id=quiz_id).category for quiz_id in quiz_ids]  # 퀴즈 ID로 각 퀴즈의 카테고리 가져오기
            category = categories[0] if categories else 1  # 카테고리가 존재하면 첫 번째 카테고리, 아니면 기본값 1

            # QuizHistroy 객체 생성 및 저장
            history = QuizHistroy(
                category=category,
                is_passed=is_passed,
                user_id=request.user  # 현재 로그인된 사용자 객체
            )
            history.save()

            # 디버깅 정보 출력
            print(f'QuizHistroy saved: {history}')

            # QuizHistroyItem 객체 생성 및 저장
            for idx, answer in enumerate(answers):
                quiz = Quiz.objects.get(id=quiz_ids[idx])
                item = QuizHistroyItem.objects.create(
                    education_quiz_histroy_id=history,
                    education_quiz_id=quiz,
                    answer=answer
                )

                # 디버깅 정보 출력
                print(f'QuizHistroyItem saved: {item}')

            return JsonResponse({'results': results})  # 결과를 JSON 형태로 반환

    else:
        form = QuizForm()

    return render(request, 'education/quiz.html', {'quizzes': quizzes, 'form': form})  # GET 요청일 경우 퀴즈 페이지 렌더링



# 웹에서 동작하는 Chatbot 초기화 메시지
messages = (
    "너는 통신회사의 고객센터 상담사를 육성하는 챗봇이다. "
    "'시작'이라는 신호를 받으면 고객센터에 전화하는 고객 역할을 맡고, 나에게 민원을 제기한다. "
    "나의 답변을 듣고, 그 답변에 대해 교육자의 입장에서 평가를 해준다. 그런 다음 다시 고객 역할로 돌아가서 다음 연관 질문을 던진다. "
    "정확하고 친절하게 고객의 역할을 수행하고, 교육자의 평가에서는 구체적이고 도움이 되는 피드백을 제공하도록 한다. "
    "질문이 명확하지 않으면 추가 정보를 요청할 수 있다. "
    "고객의 역할을 수행할 때는 다양한 민원 사항을 제기하며, 명확하고 구체적인 질문을 던진다. "
    "고객이 명세서를 확인할 수 있는 방법과 구체적인 확인 사항을 안내하고, 문제 해결을 위한 추가 조치를 제시한다."
)

chatbot = Chatbot(os.getenv("OPENAI_API_KEY"), 'database/chroma.sqlite3')  # Chatbot 객체 생성

# 퀴즈 이력
@login_required
def quiz_history(request):
    logs = QuizHistroy.objects.all().select_related('user_id')  # user_id 필드에 대한 역참조를 포함
    
    # 검색 필터링 처리
    search_text = request.GET.get('searchText', '')
    category = request.GET.get('category', '')
    result = request.GET.get('result', '')

    if search_text:
        logs = logs.filter(
            Q(user_id__username__icontains=search_text) |
            Q(user_id__name__icontains=search_text)
        )

    if category:
        logs = logs.filter(category=category)
    
    if result:
        if result == 'pass':
            logs = logs.filter(is_passed=True)
        elif result == 'fail':
            logs = logs.filter(is_passed=False)

    # 페이지네이션 처리
    paginator = Paginator(logs, 10)  # 페이지당 10개씩 표시
    page = request.GET.get('page')
    logs = paginator.get_page(page)

    return render(request, 'education/quiz_history.html', {
        'logs': logs,
        'is_paginated': logs.has_other_pages()
    })

# 퀴즈 이력 상세
@login_required
def quiz_details(request, log_id):

    # 퀴즈 내역을 그대로 복원해서 html에 뿌려주세요 - ㅎㅅ
    # quizhistory id == historyitems에 quiz_histo_id 에 quiz_id == quiz id 문제를 출력 해야 합니다. 
    # 아래는 임시 
    # log = get_object_or_404(QuizHistroy, id=log_id)
    # items = QuizHistroyItem.objects.filter(quiz_history=log).select_related('quiz')
    # return render(request, 'education/quiz_details.html', {'log': log, 'items': items})
    
    log = get_object_or_404(QuizHistroy, id=log_id)
    return render(request, 'education/quiz_details.html', {'log': log})

# Chatbot 뷰
def chat_view(request):
    global chatbot
    if request.method == 'POST':
        if 'category' in request.POST:
            category = request.POST.get('category')
            api_key = os.environ['OPENAI_API_KEY']
            db_path = '../db'

            # Chatbot 객체 초기화
            chatbot = Chatbot(
                api_key=api_key, 
                db_path=db_path, 
                category=category, 
                THRESHOLD=2,
                behavior_policy=messages
            )

            # 첫 질문 생성
            initial_question = chatbot.chat("고객의 역할에서 민원을 말해줘")
            return JsonResponse({'status': 'success', 'initial_question': initial_question})

        elif 'message' in request.POST:
            message = request.POST.get('message')

            if chatbot is None:
                return JsonResponse({'response': 'Chatbot is not initialized. Please select a category first.'})

            # 사용자 메시지에 대한 응답 생성
            output = chatbot.chat(message)
            return JsonResponse({'response': output})

    return render(request, 'education/index.html')