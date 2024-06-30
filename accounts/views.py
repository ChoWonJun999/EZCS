from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from django.contrib.auth import authenticate
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            print(user.password)
            if password == user.password:
                result = 'success'
            else:
                result = 'Incorrect password'
        except User.DoesNotExist:
            result = 'User does not exist'

        return JsonResponse({'result': result})
    return render(request, 'accounts/login.html')