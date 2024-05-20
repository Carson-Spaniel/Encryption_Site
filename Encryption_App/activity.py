from django.contrib.auth import logout
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity_str = request.session.get('last_activity')
            if last_activity_str:
                last_activity = datetime.fromisoformat(last_activity_str)
                current_time = timezone.now()

                if (current_time - last_activity).seconds > settings.SESSION_EXPIRE_SECONDS:
                    messages.error(request, "Logged out due to inactivity.")
                    logout(request)
                    return redirect(reverse('login_page'))

        response = self.get_response(request)

        if request.user.is_authenticated:
            request.session['last_activity'] = timezone.now().isoformat()

        return response
