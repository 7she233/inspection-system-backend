from rest_framework import serializers
from .models import Inspection, Event, MediaFile

class MediaFileSerializer(serializers.ModelSerializer):
    """媒体文件序列化器"""
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = MediaFile
        fields = ['id', 'type', 'type_display', 'url', 'duration', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']

class EventSerializer(serializers.ModelSerializer):
    """事件序列化器"""
    media_files = MediaFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'inspection', 'description', 'manual_description', 
                 'ai_analysis', 'created_at', 'updated_at', 'media_files']
        read_only_fields = ['id', 'created_at', 'updated_at']

class InspectionListSerializer(serializers.ModelSerializer):
    """巡检列表序列化器"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    inspector_name = serializers.CharField(source='inspector.nickname', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    event_count = serializers.IntegerField(source='events.count', read_only=True)

    class Meta:
        model = Inspection
        fields = ['id', 'title', 'location', 'status', 'status_display', 
                 'inspector_name', 'start_time', 'created_at', 'event_count']
        read_only_fields = ['id', 'created_at', 'event_count']

class InspectionDetailSerializer(serializers.ModelSerializer):
    """巡检详情序列化器"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    inspector_name = serializers.CharField(source='inspector.nickname', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    events = EventSerializer(many=True, read_only=True)
    event_count = serializers.IntegerField(source='events.count', read_only=True)

    class Meta:
        model = Inspection
        fields = ['id', 'title', 'location', 'latitude', 'longitude', 'summary',
                 'status', 'status_display', 'inspector', 'inspector_name',
                 'start_time', 'end_time', 'created_at', 'updated_at',
                 'events', 'event_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'inspector_name', 'event_count'] 