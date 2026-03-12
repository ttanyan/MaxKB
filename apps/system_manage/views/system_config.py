# coding=utf-8
"""
    @project: MaxKB
    @Author：系统配置
    @file： system_config.py
    @date：2025/3/9
    @desc: 系统配置视图
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from common.result import result
from system_manage.serializers.system import SystemConfigSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_system_config(request):
    """
    获取系统配置信息
    """
    return result.success(SystemConfigSerializer.get_config())
