from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Inspection(models.Model):
    """巡检记录"""
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('archived', '已归档')
    )

    id = models.CharField(primary_key=True, max_length=32, help_text="巡检ID")
    title = models.CharField(max_length=100, help_text="巡检标题")
    location = models.CharField(max_length=255, help_text="巡检地点")
    latitude = models.FloatField(null=True, blank=True, help_text="纬度")
    longitude = models.FloatField(null=True, blank=True, help_text="经度")
    inspector = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='inspections',
        help_text="巡检人员"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='draft',
        help_text="巡检状态"
    )
    start_time = models.DateTimeField(null=True, blank=True, help_text="开始时间")
    end_time = models.DateTimeField(null=True, blank=True, help_text="结束时间")
    summary = models.TextField(blank=True, help_text="巡检总结")
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, help_text="更新时间")

    class Meta:
        ordering = ['-created_at']
        db_table = 'inspection'
        verbose_name = '巡检记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def start(self):
        """开始巡检"""
        if self.status != 'draft':
            raise ValueError('只有草稿状态可以开始巡检')
        self.status = 'in_progress'
        self.start_time = timezone.now()
        self.save()

    def complete(self):
        """完成巡检"""
        if self.status != 'in_progress':
            raise ValueError('只有进行中的巡检可以完成')
        self.status = 'completed'
        self.end_time = timezone.now()
        self.save()

    def archive(self):
        """归档巡检"""
        if self.status != 'completed':
            raise ValueError('只有已完成的巡检可以归档')
        self.status = 'archived'
        self.save()


class Event(models.Model):
    """事件"""
    id = models.CharField(primary_key=True, max_length=32, help_text="事件ID")
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='events', help_text="所属巡检")
    description = models.TextField(blank=True, help_text="问题描述")
    manual_description = models.TextField(blank=True, help_text="手工输入的描述")
    ai_analysis = models.TextField(blank=True, help_text="AI分析结果")
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, help_text="更新时间")

    class Meta:
        ordering = ['created_at']
        db_table = 'event'
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
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='media_files', help_text="所属事件")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, help_text="文件类型")
    url = models.URLField(help_text="文件URL")
    duration = models.IntegerField(null=True, blank=True, help_text="语音时长(秒)")
    text = models.TextField(blank=True, help_text="语音识别文本")
    local_path = models.CharField(max_length=255, blank=True, help_text="本地文件路径")
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")

    class Meta:
        ordering = ['created_at']
        db_table = 'media_file'
        verbose_name = '媒体文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.get_type_display()} {self.id}" 