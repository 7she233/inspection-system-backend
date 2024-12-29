from django.utils import timezone
from .models import User

class UserStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            # 更新最后登录时间
            User.objects.filter(id=request.user.id).update(
                last_login_time=timezone.now()
            )
        return self.get_response(request) 