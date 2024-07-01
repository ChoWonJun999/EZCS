from django.shortcuts import render

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