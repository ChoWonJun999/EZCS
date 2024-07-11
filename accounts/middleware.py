from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
import time


class BlockedMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.session.get('blocked'):
            messages.info(request, '다른 기기에서 동일아이디로 로그인되어 자동으로 로그아웃 되었습니다.')
            request.session.pop('blocked')
            logout(request)
            return redirect(settings.LOGIN_URL)


class LoginSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in ['/favicon.ico'] or 'logout' in request.path:
            return None
        
        user = request.user.id

        if 'accounts' in request.path:
            if user:
                return redirect(reverse("main:user_dashboard"))
            return None
        
        if not user:
            return redirect(reverse("accounts:login"))
        
        if not request.user.is_superuser and 'management' in request.path:
            return redirect(reverse("accounts:login"))

        return None


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
        
        request.session['last_activity'] = current_time
        request.session.modified = True
