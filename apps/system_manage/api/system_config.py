# coding=utf-8
"""
    @project: MaxKB
    @Author：系统配置
    @file： system_config.py
    @date：2025/3/9
    @desc: 系统配置 API
"""
from common.mixins.api_mixin import APIMixin
from common.result import ResultSerializer
from system_manage.serializers.system import SystemConfigSerializer


class SystemConfigResult(ResultSerializer):
    def get_data(self):
        return SystemConfigSerializer.get_config()


class SystemConfigAPI(APIMixin):
    @staticmethod
    def get_response():
        return SystemConfigResult
