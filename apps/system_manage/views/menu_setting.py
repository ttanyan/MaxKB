# coding=utf-8
"""
    @project: MaxKB
    @Author：Codex
    @file： menu_setting.py
    @date：2026/3/13
    @desc: 菜单管理视图
"""
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from common.auth import TokenAuth
from common.auth.authentication import has_permissions
from common.constants.permission_constants import PermissionConstants, RoleConstants
from common.log.log import log
from common.result import result
from django.utils.translation import gettext_lazy as _

from system_manage.api.menu_setting import MenuSettingAPI, MenuSettingUpdateAPI, CurrentMenuSettingAPI
from system_manage.serializers.menu_setting import MenuSettingSerializer


def get_menu_setting_details(request):
    return {
        'path': request.path,
        'body': request.data,
        'query': request.query_params
    }


class MenuSettingView(APIView):
    authentication_classes = [TokenAuth]

    @extend_schema(methods=['GET'],
                   summary=_('Get menu settings'),
                   description=_('Get menu settings'),
                   operation_id=_('Get menu settings'),  # type: ignore
                   responses=MenuSettingAPI.get_response(),
                   tags=[_('Menu Settings')])  # type: ignore
    @has_permissions(PermissionConstants.USER_READ, RoleConstants.ADMIN)
    def get(self, request: Request):
        return result.success(MenuSettingSerializer.get_config())

    @extend_schema(methods=['PUT'],
                   summary=_('Update menu settings'),
                   description=_('Update menu settings'),
                   operation_id=_('Update menu settings'),  # type: ignore
                   request=MenuSettingUpdateAPI.get_request(),
                   responses=MenuSettingUpdateAPI.get_response(),
                   tags=[_('Menu Settings')])  # type: ignore
    @log(menu='Menu management', operate='Update menu settings', get_details=get_menu_setting_details)
    @has_permissions(PermissionConstants.USER_EDIT, RoleConstants.ADMIN)
    def put(self, request: Request):
        return result.success(MenuSettingSerializer.Update(data=request.data).save())


class CurrentMenuSettingView(APIView):
    authentication_classes = [TokenAuth]

    @extend_schema(methods=['GET'],
                   summary=_('Get current user menu settings'),
                   description=_('Get current user menu settings'),
                   operation_id=_('Get current user menu settings'),  # type: ignore
                   responses=CurrentMenuSettingAPI.get_response(),
                   tags=[_('Menu Settings')])  # type: ignore
    def get(self, request: Request):
        return result.success({'menu_list': MenuSettingSerializer.get_current_menu_list(request.user)})
