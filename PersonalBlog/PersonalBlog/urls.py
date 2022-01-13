from django.urls import path, include
from rest_framework.routers import DefaultRouter
from article.views import ArticleViewSet, CategoryViewSet, TagViewSet, AvatarViewSet
from comment.views import CommentViewSet
from user_info.views import UserRegisterViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'article', ArticleViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'tag', TagViewSet)
router.register(r'avatar', AvatarViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'user', UserRegisterViewSet)

urlpatterns = [
    # drf 自动注册路由
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
