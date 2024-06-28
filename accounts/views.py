from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from accounts.models import User

def login_view(request):
    if request.method == 'POST' and request.is_ajax():
        result = 'success'        
        user = User.objects.filter(id=request.POST['id'], pw=request.Post['pw'])
        
        if not user.exists():
            result = 'No Exists'
            context = {'result': result}
            return JsonResponse(context, status=401)
        else:
            response = JsonResponse({'result': result})
            return response
    
    return render(request, 'accounts/login.html')
