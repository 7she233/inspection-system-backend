from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except AuthenticationFailed as e:
            if str(e) == 'Token is invalid or expired':
                raise AuthenticationFailed({
                    'code': 401,
                    'message': '登录已过期，请重新登录'
                })
            raise e 