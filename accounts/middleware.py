from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as auth_logout


class BlockedMiddleware(MiddlewareMixin):
    def process_request(self, request):
        blocked = request.session.pop('blocked', None)
        if blocked:
            messages.info(request, '다른 기기에서 동일아이디로 로그인되어 자동으로 로그아웃 되었습니다.')
            auth_logout(request)
            return redirect(settings.LOGIN_URL)


class LoginSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/favicon.ico' or 'logout' in request.path:
            return self.get_response(request)

        user = request.session.get('user', None)

        if 'accounts' in request.path:
            if user:
                return redirect("/")
            return self.get_response(request)
        
        if not user:
            return redirect("/accounts/")
        
        response = self.get_response(request)

        if response is None:
            response = HttpResponse("Internal Server Error", status=500)

        return response

