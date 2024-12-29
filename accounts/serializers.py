from rest_framework import serializers
from .models import Inspection

class InspectionListSerializer(serializers.ModelSerializer):
    """巡检列表序列化器"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    inspector_name = serializers.CharField(source='inspector.nickname', read_only=True)

    class Meta:
        model = Inspection
        fields = ['id', 'title', 'location', 'status', 'status_display', 
                 'inspector_name', 'start_time', 'created_at']
        read_only_fields = ['id', 'created_at']

class InspectionDetailSerializer(serializers.ModelSerializer):
    """巡检详情序列化器"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    inspector_name = serializers.CharField(source='inspector.nickname', read_only=True)
    events = serializers.SerializerMethodField()

    class Meta:
        model = Inspection
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_events(self, obj):
        from apps.events.serializers import EventSerializer
        return EventSerializer(obj.inspection_events.all(), many=True).data