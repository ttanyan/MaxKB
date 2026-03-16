# coding=utf-8
"""
    @project: MaxKB
    @Author：Codex
    @file： menu_setting.py
    @date：2026/3/13
    @desc: 菜单管理 API
"""
from common.mixins.api_mixin import APIMixin
from common.result import ResultSerializer
from system_manage.serializers.menu_setting import MenuSettingSerializer, MenuSettingResponseSerializer, \
    CurrentMenuSettingResponseSerializer


class MenuSettingResponse(ResultSerializer):
    def get_data(self):
        return MenuSettingResponseSerializer()


class MenuSettingUpdateResponse(ResultSerializer):
    def get_data(self):
        return MenuSettingSerializer.Update()


class CurrentMenuSettingResponse(ResultSerializer):
    def get_data(self):
        return CurrentMenuSettingResponseSerializer()


class MenuSettingAPI(APIMixin):
    @staticmethod
    def get_request():
        return MenuSettingSerializer.Update()

    @staticmethod
    def get_response():
        return MenuSettingResponse


class CurrentMenuSettingAPI(APIMixin):
    @staticmethod
    def get_response():
        return CurrentMenuSettingResponse


class MenuSettingUpdateAPI(APIMixin):
    @staticmethod
    def get_request():
        return MenuSettingSerializer.Update()

    @staticmethod
    def get_response():
        return MenuSettingUpdateResponse
