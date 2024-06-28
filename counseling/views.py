from django.shortcuts import render

def list(request):
    return render(request, 'counseling/index.html')