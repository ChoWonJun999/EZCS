from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
import logging
import time
from django.urls import reverse


logger = logging.getLogger(__name__)
    

class BlockedMiddleware(MiddlewareMixin):
    def process_request(self, request):
        blocked = request.session.pop('blocked', None)
        if blocked:
            messages.info(request, '다른 기기에서 동일아이디로 로그인되어 자동으로 로그아웃 되었습니다.')
            request.session.pop('user', None)
            logout(request)
            return redirect(settings.LOGIN_URL)


class LoginSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/favicon.ico' or 'logout' in request.path:
            return self.get_response(request)

        user = request.user.id

        if 'accounts' in request.path:
            if user:
                return redirect(reverse("main:user_dashboard"))
            return self.get_response(request)
        
        if not user:
            return redirect(reverse("accounts:login"))
        
        if not request.user.is_superuser and 'management' in request.path:
            return redirect(reverse("accounts:login"))

        response = self.get_response(request)

        if response is None:
            response = HttpResponse("Internal Server Error", status=500)

        return response


class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        current_time = time.time()
        session_last_activity = request.session.get('last_activity', current_time)

        if current_time - session_last_activity > settings.SESSION_COOKIE_AGE:
            messages.info(request, "로그인 세션이 만료 됐습니다. 다시 로그인 해주세요.")
            logout(request)
            return redirect(reverse("accounts:login"))
        else:
            request.session['last_activity'] = current_time

        request.session.modified = True
