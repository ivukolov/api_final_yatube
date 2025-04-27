from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Кастомный permission позволяет не атворизироолванным пользователям
    осущетсвлять запросы типа 'GET', 'HEAD', 'OPTIONS'
    и проверяет авторство объекта."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author


class OnlyAuthenticatedOrNot(BasePermission):
    """Кастомный permission запрещает доступ неавторизированным
    пользователям и проверяет авторство объекта."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author

