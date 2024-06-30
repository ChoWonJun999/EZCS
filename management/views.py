from django.shortcuts import render

def manager_dashboard(request):
    return render(request, 'main/manager_dashboard.html')