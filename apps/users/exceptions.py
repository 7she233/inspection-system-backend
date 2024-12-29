from rest_framework.exceptions import APIException
from rest_framework import status

class WeChatAPIError(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = '微信服务暂时不可用'
    default_code = 'wechat_api_error'

class UserAuthError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '用户认证失败'
    default_code = 'user_auth_error' 