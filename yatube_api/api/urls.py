from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(
    r'posts/(?P<post_id>.+)/comments',
    CommentViewSet,
    basename='comment'
)
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
]