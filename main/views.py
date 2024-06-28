from django.shortcuts import render

def user_dashboard(request):
    return render(request, 'main/index.html')

def manager_dashboard(request):
    return render(request, 'main/manager_dashboard.html')