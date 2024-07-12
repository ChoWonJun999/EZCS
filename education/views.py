import json
import logging
from datetime import datetime, timedelta

from .models import *
from .forms import QuizForm

from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from chat import Chatbot
from prompt import Prompt


logger = logging.getLogger(__name__)


chatbot = None
evaluation_chatbot = None
prompt = Prompt()
prompt.set_initial_behavior_policy_for_education()


def chat_view(request):
    '''
    교육 페이지
    '''
    if request.method == "POST":
        global chatbot
        category = request.POST.get("category", None)
        message = request.POST.get("message", None)
        if message:
            log_header_id = request.POST.get("log_header", None)
            if chatbot is None:
                return JsonResponse({"response": "Chatbot is not initialized. Please select a category first."})
            # 사용자 메시지에 대한 응답 생성
            output = chatbot.chat(message)

            evaluation_chatbot = Chatbot(
                api_key=settings.OPENAI_API_KEY,
                db_path=settings.DB_PATH,
                model_id="ft:gpt-3.5-turbo-0125:personal::9gS63IJD",
                category=category,
                THRESHOLD=2,
                behavior_policy=prompt.get_messages_for_evaluation(output, message),
            )

            evaluation_output = evaluation_chatbot.chat(message)

            LogItem.objects.create(
                chatbot=output
                , user=message
                , evaluate=evaluation_output
                , log_id=log_header_id
            )

            return JsonResponse({
                "response": output
                , "userInput": message
                , "output": evaluation_output
            })
        elif category:
            # Chatbot 객체 초기화
            chatbot = Chatbot(
                api_key=settings.OPENAI_API_KEY,
                db_path=settings.DB_PATH,
                model_id="ft:gpt-3.5-turbo-0125:personal::9gS63IJD",
                category=category,
                THRESHOLD=2,
                behavior_policy=prompt.get_behavior_policy(),
            )

            # 첫 질문 생성
            initial_question = chatbot.chat("고객의 역할에서 민원을 말해줘")
            logger.log(1, initial_question)
            if category == '모바일 > 부가서비스':
                category = 0
            elif category == '모바일 > 서비스정책':
                category = 1
            else:
                category = 2
            log_header = Log.objects.create(
                category=category
                , auth_user_id=request.user.id
            )

            LogItem.objects.create(
                chatbot=initial_question
                , log_id=log_header.id
            )
            
            return JsonResponse({
                "status": "success"
                , "initial_question": initial_question
                , "log_header": log_header.id
            })
        
    return render(request, "education/index.html")
    

def edu_history(request):
    '''
    교육 이력 페이지
    '''

    # 검색 필터링 처리
    search_text = request.GET.get("searchText", "")
    search_select = request.GET.get("searchSelect", "")
    
    start_date = request.GET.get("startDate", "")
    end_date = request.GET.get("endDate", "")

    query = Q()
    if not request.user.is_superuser:
        query = Q(auth_user=request.user.id)
    
    query1 = Q()
    if search_text:
        query1 = Q(auth_user__username__icontains=search_text)
        query1 |= Q(auth_user__first_name__icontains=search_text)

    query2 = Q()
    if search_select:
        query2 = Q(category=search_select)

    query3 = Q()
    if start_date and end_date:
        query3 &= Q(create_time__gte=start_date)
        query3 &= Q(create_time__lte=end_date)
    else:
        one_month_ago = datetime.now() - timedelta(days=30)
        query3 &= Q(create_time__gte=one_month_ago)
        query3 &= Q(create_time__lte=datetime.now())
        start_date = one_month_ago.strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

    data = Log.objects.filter(query & query1 & query2 & query3).order_by('-create_time', 'category')

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

    return render(request, "education/edu_history.html", context)


def edu_details(request, id):
    '''
    교육 이력 상세 페이지
    '''
    print("haha")
    print("haha")
    print("haha")
    print("haha")
    head = Log.objects.get(id=id)
    data = LogItem.objects.filter(log_id=id)
    context = {
        'head': head
        , 'data': data
    }
    return render(request, 'education/edu_details.html', context)


@csrf_exempt
def quiz(request):
    '''
    퀴즈페이지
    '''
    quizzes = Quiz.objects.order_by('?')[:5]  # 퀴즈 5개를 랜덤으로 가져오기

    if request.method == "POST":  # 폼 제출이 POST 요청으로 이루어질 때
        form = QuizForm(request.POST)
        if form.is_valid():
            answers = json.loads(form.cleaned_data["answers"])
            quiz_ids = [int(id) for id in json.loads(form.cleaned_data["quiz_ids"])]

            results = {}
            correct_answers = 0  # 정답 개수를 세기 위한 변수 초기화

            for idx, answer in enumerate(answers):  # 제출된 답변들을 순회하면서
                try:
                    quiz = Quiz.objects.get(id=quiz_ids[idx])  # 현재 퀴즈 ID로 퀴즈 객체 가져오기
                except Quiz.DoesNotExist:
                    # 퀴즈가 존재하지 않을 경우 오류 출력
                    print(f"Quiz with id {quiz_ids[idx]} does not exist.")
                    continue

                is_correct = False  # 초기 값은 오답으로 설정
                if (quiz.flag == 0 and quiz.answer.strip().lower() == answer.strip().lower()):  # 단답형 퀴즈의 경우
                    is_correct = True  # 정답일 경우
                    correct_answers += 1  # 정답 개수 증가
                elif (quiz.flag == 1 and str(quiz.answer) == answer):  # 객관식 퀴즈의 경우
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
            category = (categories[0] if categories else 1)  # 카테고리가 존재하면 첫 번째 카테고리, 아니면 기본값 1

            # QuizHistory 객체 생성 및 저장
            history = QuizHistory(
                category=category,
                is_passed=is_passed,
                auth_user_id=request.user.id,  # 현재 로그인된 사용자 객체
            )
            history.save()

            # 디버깅 정보 출력
            print(f"QuizHistory saved: {history}")

            # QuizHistoryItem 객체 생성 및 저장
            for idx, answer in enumerate(answers):
                quiz = Quiz.objects.get(id=quiz_ids[idx])
                item = QuizHistoryItem.objects.create(
                    quiz_history=history,
                    quiz=quiz,
                    answer=answer,
                )

                # 디버깅 정보 출력
                print(f"QuizHistoryItem saved: {item}")

            return JsonResponse({"results": results})  # 결과를 JSON 형태로 반환

    else:
        form = QuizForm()

    return render(request, 'education/quiz.html', {'quizzes': quizzes, 'form': form})


def quiz_history(request):
    '''
    퀴즈 이력
    '''
    # 검색 필터링 처리
    search_text = request.GET.get("searchText", "")
    search_select = request.GET.get("searchSelect", "")
    
    start_date = request.GET.get("startDate", "")
    end_date = request.GET.get("endDate", "")

    result = request.GET.get("result", "")

    query = Q()
    if not request.user.is_superuser:
        query = Q(auth_user_id=request.user.id)

    query1 = Q()
    if search_text:
        query1 = Q(auth_user__username__icontains=search_text)
        query1 |= Q(auth_user__name__icontains=search_text)

    query2 = Q()
    if search_select:
        query2 = Q(category=search_select)

    query3 = Q()
    if result:
        query3 = Q(is_passed=False)
        if result == "pass":
            query3 = Q(is_passed=True)

    query4 = Q()
    if start_date and end_date:
        query4 &= Q(create_time__gte=start_date)
        query4 &= Q(create_time__lte=end_date)
    else:
        one_month_ago = datetime.now() - timedelta(days=30)
        query4 &= Q(create_time__gte=one_month_ago)
        query4 &= Q(create_time__lte=datetime.now())
        start_date = one_month_ago.strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

    data = QuizHistory.objects.filter(query & query2 & query3 & query4).select_related('auth_user').order_by('-create_time', 'category')

    paginator = Paginator(data, 10)
    page = request.GET.get('page')
    data = paginator.get_page(page)

    context = {
        'data': data,
        'searchSelect': search_select,
        'searchText': search_text,
        'startDate': start_date,
        'endDate': end_date,
        'result': result,
        'is_paginated': data.has_other_pages(),
    }

    return render(request, "education/quiz_history.html", context)

def quiz_details(request, log_id):
    '''
    퀴즈 이력 상세
    '''
    log = get_object_or_404(QuizHistory, id=log_id)

    items = QuizHistoryItem.objects.filter(quiz_history=log_id).select_related('education_quiz_id')
    
    return render(request, 'education/quiz_details.html', {'log': log, 'items' : items})
