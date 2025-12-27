from rest_framework.permissions import BasePermission


class IsModers(BasePermission):

    def has_permission(self, request, view):
        """ Проверка принадлежности пользователя к группе 'Модераторы'"""
        return request.user.groups.filter(name='moders').exists()
