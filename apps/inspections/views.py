from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
import uuid
import logging

from .models import Inspection, Event
from .serializers import InspectionListSerializer, InspectionDetailSerializer, EventSerializer
from .permissions import IsInspectorOrAdmin

logger = logging.getLogger(__name__)

class InspectionViewSet(viewsets.ModelViewSet):
    """巡检视图集"""
    permission_classes = [IsAuthenticated, IsInspectorOrAdmin]
    serializer_class = InspectionDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'location']
    ordering_fields = ['created_at', 'start_time', 'end_time']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """根据用户权限返回查询集"""
        queryset = Inspection.objects.select_related('inspector')
        if not self.request.user.is_staff:
            queryset = queryset.filter(inspector=self.request.user)
        return queryset
    
    def get_serializer_class(self):
        """根据操作类型返回不同的序列化器"""
        if self.action == 'list':
            return InspectionListSerializer
        return InspectionDetailSerializer
    
    def create(self, request, *args, **kwargs):
        """创建巡检记录"""
        try:
            # 准备数据
            data = request.data.copy()
            data.update({
                'inspector': request.user.id,
                'status': 'draft',
                'id': uuid.uuid4().hex
            })
            
            # 序列化和保存
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            inspection = serializer.save()
            
            return Response(
                self.get_serializer(inspection).data,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.error(f"创建巡检失败: {str(e)}")
            return Response(
                {'detail': f'创建失败: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

class EventViewSet(viewsets.ModelViewSet):
    """事件视图集"""
    permission_classes = [IsAuthenticated, IsInspectorOrAdmin]
    serializer_class = EventSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_queryset(self):
        """获取特定巡检的事件列表"""
        inspection_id = self.kwargs.get('inspection_id')
        return Event.objects.filter(inspection_id=inspection_id) 