from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.http import HttpResponse


class BlockedMiddleware(MiddlewareMixin):
    def process_request(self, request):
        blocked = request.session.pop('blocked', None)
        print(f"blocked : {blocked}")
        if blocked:
            request.session.pop('user')
            return redirect('/')


class LoginSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"request.path : {request.path}")
        if request.path == '/favicon.ico' or 'logout' in request.path:
            return self.get_response(request)

        user = request.session.get('user', None)
        print(f"user : {user}")

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

