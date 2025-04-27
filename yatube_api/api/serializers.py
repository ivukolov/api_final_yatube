from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        read_only_fields = ('author', 'post', 'created')
        fields = ['id', 'author', 'post', 'text', 'created']


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    user = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Follow
        read_only_fields = ('user', )
        fields = ('user', 'following')

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя"
            )
        if Follow.objects.filter(
            user=self.context['request'].user, following=data['following']
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя"
            )
        return data
