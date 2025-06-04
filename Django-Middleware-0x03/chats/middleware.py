import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.conf import settings

# Configure logging to write to requests.log
logging.basicConfig(
    filename=settings.BASE_DIR / 'requests.log',
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if not (9 <= current_hour < 18):  # Allow access between 9 AM and 6 PM
            return HttpResponseForbidden("Chat access is restricted outside 9 AM to 6 PM.")
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and 'messages' in request.path:
            client_ip = request.META.get('REMOTE_ADDR')
            cache_key = f"message_count_{client_ip}"
            message_count = cache.get(cache_key, 0)
            
            if message_count >= 5:
                return HttpResponseForbidden("Message limit exceeded: 5 messages per minute.")
            
            # Increment count and set 1-minute expiry
            cache.set(cache_key, message_count + 1, timeout=60)
            
        response = self.get_response(request)
        return response

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/conversations/') or request.path.startswith('/api/messages/'):
            if not (request.user.is_authenticated and (request.user.is_staff or hasattr(request.user, 'is_moderator'))):
                return HttpResponseForbidden("Only admins or moderators can access this action.")
        response = self.get_response(request)
        return response