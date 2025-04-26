from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from posts.models import Post, Comment, Group
from api.serializers import PostSerializer, GroupSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


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
