from rest_framework import permissions

class IsInspectorOrAdmin(permissions.BasePermission):
    """
    自定义权限类：
    - 管理员可以访问所有巡检记录
    - 普通用户只能访问自己创建的巡检记录
    """
    def has_permission(self, request, view):
        # 所有认证用户都可以创建巡检
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 检查对象级权限
        return request.user.is_staff or obj.inspector == request.user 