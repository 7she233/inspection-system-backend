from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import requests
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def wechat_login(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'error': '缺少code参数'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # 获取微信用户信息
            wx_response = requests.get(
                'https://api.weixin.qq.com/sns/jscode2session',
                params={
                    'appid': settings.WECHAT_APP_ID,
                    'secret': settings.WECHAT_APP_SECRET,
                    'js_code': code,
                    'grant_type': 'authorization_code'
                }
            )
            wx_data = wx_response.json()
            
            if 'errcode' in wx_data:
                return Response({'error': '微信登录失败'}, status=status.HTTP_400_BAD_REQUEST)
                
            # 获取或创建用户
            user, created = User.objects.get_or_create(
                openid=wx_data['openid'],
                defaults={
                    'username': f"wx_{wx_data['openid'][:8]}",
                    'unionid': wx_data.get('unionid', ''),
                }
            )
            
            # 生成JWT令牌
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id) 