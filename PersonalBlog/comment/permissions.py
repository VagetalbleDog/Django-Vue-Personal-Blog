from rest_framework import permissions


# ”“”传统写法“”“
# class IsOwnerOrReadOnly(permissions.BasePermission):
#     message = "必须是评论作者才可以进行相关操作"
#
#     # 进行非安全请求时，由于需要验证当前评论的作者和当前登录的用户是否为同一个人，下面的obj为评论的instance
#     # 但是存在一个问题，此方法晚于视图集中的perform_create方法，导致用户为登录新建评论时，可能导致500错误,所以需要加入下面这个函数
#     def has_object_permission(self, request, view, obj):  # 钩子函数
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.author == request.user
#
#     # 下面的方法早于视图集中的perform_create方法，避免500错误
#     def has_permission(self, request, view):  # 钩子函数
#         # 对所有人允许GET，HEAD，OPTIONS请求
#         if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
#             return True
#         return request.user.is_authenticated


# 代码重构,使用闭包和lambda匿名函数
class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "必须是评论作者才可以进行相关操作"

    def safe_methods_or_owner(self, request, func):
        if request.method in permissions.SAFE_METHODS:
            return True
        return func()

    def has_permission(self, request, view):
        return self.safe_methods_or_owner(
            request,
            lambda: request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return self.safe_methods_or_owner(
            request,
            lambda: obj.author == request.user
        )
