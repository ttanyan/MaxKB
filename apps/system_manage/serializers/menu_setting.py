# coding=utf-8
"""
    @project: MaxKB
    @Author：Codex
    @file： menu_setting.py
    @date：2026/3/13
    @desc: 菜单管理序列化器
"""
from collections import OrderedDict

from django.db import transaction, OperationalError, ProgrammingError
from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from common.constants.permission_constants import RoleConstants
from common.exception.app_exception import AppApiException
from system_manage.models import UserMenuSetting
from users.models import User


MENU_TREE = [
    {
        'id': 'main-navigation-group',
        'label': '主导航',
        'description': '对应 /admin/application 左侧主菜单',
        'children': [
            {'id': 'application', 'label': 'AI应用', 'description': '左侧主导航 / AI应用'},
            {'id': 'mindmap', 'label': '思维导图', 'description': '左侧主导航 / 思维导图'},
            {'id': 'knowledge', 'label': '知识库', 'description': '左侧主导航 / 知识库'},
            {'id': 'tool', 'label': '工具管理', 'description': '左侧主导航 / 工具管理'},
            {'id': 'model', 'label': '模型管理', 'description': '左侧主导航 / 模型管理'},
        ],
    },
]


def get_leaf_ids(menu_tree):
    leaf_ids = []
    for item in menu_tree:
        children = item.get('children') or []
        if children:
            leaf_ids.extend(get_leaf_ids(children))
        else:
            leaf_ids.append(item.get('id'))
    return leaf_ids


ALL_MENU_LIST = get_leaf_ids(MENU_TREE)


class MenuSettingUserSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True, label=_('User ID'))
    nick_name = serializers.CharField(required=True, label=_('Nick name'))
    username = serializers.CharField(required=True, label=_('Username'))
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True, label=_('Email'))
    is_active = serializers.BooleanField(required=True, label=_('Is active'))


class MenuSettingResponseSerializer(serializers.Serializer):
    menu_tree = serializers.ListField(required=True, label=_('Menu tree'))
    users = MenuSettingUserSerializer(many=True, required=True, label=_('User list'))
    checked_map = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField(required=True)),
        required=True,
        label=_('User menu mapping')
    )


class CurrentMenuSettingResponseSerializer(serializers.Serializer):
    menu_list = serializers.ListField(child=serializers.CharField(required=True), required=True, label=_('Menu list'))


class MenuSettingSerializer(serializers.Serializer):
    @staticmethod
    def _is_system_admin(user_or_role):
        role = getattr(user_or_role, 'role', user_or_role)
        return role == RoleConstants.ADMIN.name

    @staticmethod
    def get_menu_tree():
        return MENU_TREE

    @staticmethod
    def get_default_menu_list():
        return ['knowledge']

    @staticmethod
    def _get_admin_menu_list():
        return list(ALL_MENU_LIST)

    @staticmethod
    def _normalize_menu_list(menu_list):
        valid_ids = set(ALL_MENU_LIST)
        unique_menu_list = OrderedDict()
        for menu_id in menu_list:
            if menu_id in valid_ids:
                unique_menu_list[menu_id] = True
        return list(unique_menu_list.keys())

    @staticmethod
    def _get_user_queryset():
        return User.objects.exclude(role=RoleConstants.ADMIN.name).order_by('create_time', 'username')

    @staticmethod
    def _get_checked_map(users=None):
        checked_map = {}
        if users is not None:
            default_menu_list = MenuSettingSerializer.get_default_menu_list()
            checked_map = {str(user.id): list(default_menu_list) for user in users}
        try:
            for setting in UserMenuSetting.objects.select_related('user').exclude(user__role=RoleConstants.ADMIN.name):
                checked_map[str(setting.user_id)] = MenuSettingSerializer._normalize_menu_list(setting.menu_list or [])
        except (ProgrammingError, OperationalError):
            return checked_map
        return checked_map

    @staticmethod
    def get_config():
        user_queryset = list(MenuSettingSerializer._get_user_queryset())
        users = list(user_queryset)
        return {
            'menu_tree': MenuSettingSerializer.get_menu_tree(),
            'users': [{
                'id': user.id,
                'nick_name': user.nick_name,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active
            } for user in users],
            'checked_map': MenuSettingSerializer._get_checked_map(user_queryset)
        }

    @staticmethod
    def get_current_menu_list(user):
        if MenuSettingSerializer._is_system_admin(user):
            return MenuSettingSerializer._get_admin_menu_list()
        user_id = getattr(user, 'id', user)
        try:
            setting = UserMenuSetting.objects.filter(user_id=user_id).first()
            if setting is None:
                return MenuSettingSerializer.get_default_menu_list()
            return MenuSettingSerializer._normalize_menu_list(setting.menu_list or [])
        except (ProgrammingError, OperationalError):
            return MenuSettingSerializer.get_default_menu_list()

    class Update(serializers.Serializer):
        user_id = serializers.UUIDField(required=True, label=_('User ID'))
        menu_list = serializers.ListField(
            child=serializers.CharField(required=True),
            required=True,
            allow_empty=True,
            label=_('Menu list')
        )

        def validate_user_id(self, value):
            user = User.objects.filter(id=value).first()
            if user is None:
                raise AppApiException(1004, _('User does not exist'))
            if MenuSettingSerializer._is_system_admin(user):
                raise AppApiException(500, _('System administrator menu does not support configuration'))
            return value

        def validate_menu_list(self, value):
            return MenuSettingSerializer._normalize_menu_list(value)

        @transaction.atomic
        def save(self):
            self.is_valid(raise_exception=True)
            user_id = self.validated_data.get('user_id')
            menu_list = self.validated_data.get('menu_list')
            default_menu_list = MenuSettingSerializer.get_default_menu_list()
            if menu_list == default_menu_list:
                UserMenuSetting.objects.filter(user_id=user_id).delete()
                return {'user_id': str(user_id), 'menu_list': menu_list}
            setting, _ = UserMenuSetting.objects.get_or_create(user_id=user_id)
            setting.menu_list = menu_list
            setting.save()
            return {'user_id': str(user_id), 'menu_list': setting.menu_list}
