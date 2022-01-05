from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """要么是管理员，要么只读"""
    # 实现父类钩子方法
    def has_permission(self, request, view):
        # 对所有人允许GET，HEAD，OPTIONS请求
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser
