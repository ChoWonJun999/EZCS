from django.shortcuts import render

def user_dashboard(request):
    user = request.session.get('user', None)

    data = {
        'user': user
    }
    
    return render(request, 'main/index.html', data)
