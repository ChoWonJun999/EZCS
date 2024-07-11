import json
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import QuizForm
from chat import Chatbot
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
import logging
from django.conf import settings


logger = logging.getLogger(__name__)


behavior_policy = "당신은 콜센터 상담사에게 질문을 하기 위해 전화한 고객입니다. 콜센터 상담사에게 궁금했던 내용을 질문하세요. 질문은 한 번에 한 개씩만 하세요. 질문에 대한 원하는 답변이 나왔다면 마무리 인사를 하세요."

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


def chat_view(request):
    '''
    Chatbot 뷰
    '''
    global chatbot
    if request.method == "POST":
        category = request.POST.get("category", None)
        message = request.POST.get("message", None)
        if category:
            # Chatbot 객체 초기화
            chatbot = Chatbot(
                api_key=settings.OPENAI_API_KEY,
                db_path=settings.DB_PATH,
                category=category,
                THRESHOLD=2,
                behavior_policy=behavior_policy,
            )

            # 첫 질문 생성
            initial_question = chatbot.chat("고객의 역할에서 민원을 말해줘")
            logger.log(1, initial_question)
            return JsonResponse(
                {"status": "success", "initial_question": initial_question}
            )
        elif message:
            if chatbot is None:
                return JsonResponse(
                    {
                        "response": "Chatbot is not initialized. Please select a category first."
                    }
                )
            # 사용자 메시지에 대한 응답 생성
            output = chatbot.chat(message)
            return JsonResponse({"response": output})

    return render(request, "education/index.html")


def list(request):
    '''
    교육 페이지
    '''
    return render(request, 'education/index.html')

def edu_history(request):
    '''
    교육 이력 페이지
    '''
    logs = EducationChatbotLog.objects.all()
    return render(request, 'education/edu_history.html', {'logs': logs})

# 롤플레잉 저장 함수 - 미완성
@csrf_exempt
def save_chat_data(request):
    if request.method == "POST":
        user = request.user
        category = request.POST.get("category")
        chat = request.POST.get("chat")

        body = {"category": category, "chat": chat}

        EducationChatbotLog.objects.create(user_id=user, body=body)

        return JsonResponse({"message": "Data saved successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)


def edu_details(request):
    '''
    교육 이력 상세 페이지
    '''
    return render(request, 'education/edu_details.html')

 
@csrf_exempt
@login_required
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

            # 디버깅 정보 출력
            print(f"answers: {answers}")
            print(f"quiz_ids: {quiz_ids}")

            results = {}
            correct_answers = 0  # 정답 개수를 세기 위한 변수 초기화

            for idx, answer in enumerate(answers):  # 제출된 답변들을 순회하면서
                try:
                    quiz = Quiz.objects.get(
                        id=quiz_ids[idx]
                    )  # 현재 퀴즈 ID로 퀴즈 객체 가져오기
                except Quiz.DoesNotExist:
                    # 퀴즈가 존재하지 않을 경우 오류 출력
                    print(f"Quiz with id {quiz_ids[idx]} does not exist.")
                    continue

                is_correct = False  # 초기 값은 오답으로 설정
                if (
                    quiz.flag == 0
                    and quiz.answer.strip().lower() == answer.strip().lower()
                ):  # 단답형 퀴즈의 경우
                    is_correct = True  # 정답일 경우
                    correct_answers += 1  # 정답 개수 증가
                elif (
                    quiz.flag == 1 and str(quiz.answer) == answer
                ):  # 객관식 퀴즈의 경우
                    is_correct = True  # 정답일 경우
                    correct_answers += 1  # 정답 개수 증가
                
                results[quiz.id] = {  # 결과 딕셔너리에 현재 퀴즈의 정답 여부와 사용자의 답변 저장
                    'is_correct': is_correct,
                    'user_answer': answer,
                    'commentary': quiz.commentary,  # 해설 추가
                    'correct_answer': quiz.answer
                }

            is_passed = correct_answers >= 3  # 3개 이상의 정답이면 통과로 설정
            categories = [
                Quiz.objects.get(id=quiz_id).category for quiz_id in quiz_ids
            ]  # 퀴즈 ID로 각 퀴즈의 카테고리 가져오기
            category = (
                categories[0] if categories else 1
            )  # 카테고리가 존재하면 첫 번째 카테고리, 아니면 기본값 1

            # QuizHistroy 객체 생성 및 저장
            history = QuizHistroy(
                category=category,
                is_passed=is_passed,
                user_id=request.user,  # 현재 로그인된 사용자 객체
            )
            history.save()

            # 디버깅 정보 출력
            print(f"QuizHistroy saved: {history}")


            # QuizHistroyItem 객체 생성 및 저장
            for idx, answer in enumerate(answers):
                quiz = Quiz.objects.get(id=quiz_ids[idx])
                item = QuizHistroyItem.objects.create(
                    education_quiz_histroy_id=history,
                    education_quiz_id=quiz,
                    answer=answer,
                )

                # 디버깅 정보 출력
                print(f"QuizHistroyItem saved: {item}")

            return JsonResponse({"results": results})  # 결과를 JSON 형태로 반환

    else:
        form = QuizForm()

    return render(request, 'education/quiz.html', {'quizzes': quizzes, 'form': form})  # GET 요청일 경우 퀴즈 페이지 렌더링


@login_required
def quiz_history(request):
    '''
    퀴즈 이력
    '''
    logs = QuizHistroy.objects.all().select_related('user_id')  # user_id 필드에 대한 역참조를 포함
    
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
        "education/quiz_history.html",
        {"logs": logs, "is_paginated": logs.has_other_pages()},
    )


 
@login_required
def quiz_details(request, log_id):
    '''
    퀴즈 이력 상세
    '''
    log = get_object_or_404(QuizHistroy, id=log_id)

    items = QuizHistroyItem.objects.filter(education_quiz_histroy_id=log_id).select_related('education_quiz_id')
    
    return render(request, 'education/quiz_details.html', {'log': log, 'items' : items})





def search(request):
    '''
    검색로직
    '''
    query = request.POST.get('searchText', '')
   
    if query:
        results = User.objects.filter(name__icontains=query)
    else:
        results = []
    return render(
        request, "education/edu_history.html", {"data": results, "query": query}
    )


@csrf_exempt
def evaluation_chat(request):
    """답변을 평가하는 메소드

    Args:
        request (_type_): _description_
    """
    global chatbot
    if request.method == "POST":
        customerQuestion = request.POST.get("customerQuestion")
        userInput = request.POST.get("userInput")
        print(f"###############\n{customerQuestion}\n{userInput}\n###############")
        if customerQuestion and userInput:
            category = request.POST.get("category")
            api_key = os.environ["OPENAI_API_KEY"]
            db_path = "../db"

            messages = f"""당신은 고객 서비스 평가 시스템입니다. 고객 질문에 대한 상담사의 답변을 다음 기준에 따라 평가하세요:

                        
            정확성 (Accuracy): 상담사의 답변이 고객 질문에 대해 정확하고 올바른 정보를 제공하는지 평가하세요.
            점수: 1 (부정확) ~ 5 (매우 정확)
            만약 상담사의 답변이 부정확하다면, 정확한 답변 내용을 제공하세요.

                        
            친절함 (Politeness): 상담사의 답변이 얼마나 친절하고 예의 바르게 작성되었는지 평가하세요.
            점수: 1 (불친절) ~ 5 (매우 친절)

                        
            문제 해결 능력 (Problem Solving): 상담사의 답변이 고객의 문제를 얼마나 효과적으로 해결하는지 평가하세요.
            점수: 1 (해결 불가) ~ 5 (완벽히 해결)

                        
            추가 정보 제공 (Additional Information): 상담사가 고객의 이해를 돕기 위해 추가적인 유용한 정보를 제공하는지 평가하세요.
            점수: 1 (추가 정보 없음) ~ 5 (매우 유용한 추가 정보)

                        
            응답 시간 (Response Time): 상담사의 답변이 얼마나 신속하게 제공되었는지 평가하세요.
            점수: 1 (매우 느림) ~ 5 (매우 빠름)

                        아래에 고객의 질문과 상담사의 답변이 있습니다. 각 항목에 대해 점수를 매기고, 그 이유를 간단히 설명하세요.

                        고객의 질문:
                        {customerQuestion}

                        상담사의 답변:
                        {userInput}

                        평가:
                        
            정확성: [점수] - [이유]정확한 답변: [정확한 답변 내용]
            친절함: [점수] - [이유]
            문제 해결 능력: [점수] - [이유]
            추가 정보 제공: [점수] - [이유]
            응답 시간: [점수] - [이유]
            """

            # Chatbot 객체 초기화
            chatbot = Chatbot(
                api_key=api_key,
                db_path=db_path,
                category=category,
                THRESHOLD=2,
                behavior_policy=messages,
            )

            output = chatbot.chat(userInput)

            return JsonResponse({"userInput": userInput, "output": output})

    return JsonResponse({"error": "Invalid request"}, status=400)