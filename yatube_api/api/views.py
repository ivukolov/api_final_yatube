from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django.conf import settings
from django.contrib.auth import get_user_model

from posts.models import (
    Post,
    Comment,
    Group,
    Follow
)
from api.serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)
from .permissions import IsAuthorOrReadOnly, OnlyAuthenticatedOrNot

user = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly, )
    pagination_class = LimitOffsetPagination
    page_size = settings.API_PAGE_SIZE

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthorOrReadOnly, )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def get_queryset(self):
        post = self.get_post_queryset()
        return Comment.objects.filter(post_id=post.id)

    def perform_create(self, serializer):
        post = self.get_post_queryset()
        serializer.save(author=self.request.user, post=post)

    def get_post_queryset(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    permission_classes = (OnlyAuthenticatedOrNot, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^following__username', )

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"detail": "Доступ к отдельным объектам по ID запрещен"},
            status=status.HTTP_404_NOT_FOUND
        )
