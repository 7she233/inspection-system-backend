from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Event(models.Model):
    """事件点"""
    id = models.CharField(primary_key=True, max_length=32, help_text="事件ID")
    inspection = models.ForeignKey(
        'inspections.Inspection', 
        on_delete=models.CASCADE, 
        related_name='inspection_events',
        help_text="所属巡检"
    )
    description = models.TextField(blank=True, help_text="问题描述")
    manual_description = models.TextField(blank=True, help_text="手工输入的描述")
    ai_analysis = models.TextField(blank=True, help_text="AI分析结果")
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, help_text="更新时间")

    class Meta:
        ordering = ['created_at']
        db_table = 'events_event'
        verbose_name = '事件点'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"事件点 {self.id}"


class MediaFile(models.Model):
    """媒体文件"""
    TYPE_CHOICES = (
        ('voice', '语音'),
        ('photo', '照片'),
    )

    id = models.CharField(primary_key=True, max_length=32, help_text="文件ID")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_media_files', help_text="所属事件")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, help_text="文件类型")
    url = models.URLField(help_text="文件URL")
    duration = models.IntegerField(null=True, blank=True, help_text="语音时长(秒)")
    text = models.TextField(blank=True, help_text="语音识别文本")
    local_path = models.CharField(max_length=255, blank=True, help_text="本地文件路径")
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")

    class Meta:
        ordering = ['created_at']
        db_table = 'events_media_file'
        verbose_name = '媒体文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.get_type_display()} {self.id}"
