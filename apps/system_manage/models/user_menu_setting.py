# coding=utf-8
"""
    @project: MaxKB
    @Author：Codex
    @file： user_menu_setting.py
    @date：2026/3/13
    @desc: 用户菜单显示配置
"""
import uuid_utils.compat as uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from common.mixins.app_model_mixin import AppModelMixin
from users.models import User


class UserMenuSetting(AppModelMixin):
    """
    用户菜单显示配置
    """
    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="主键id")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    menu_list = ArrayField(base_field=models.CharField(max_length=128), default=list, verbose_name="菜单列表")

    class Meta:
        db_table = "user_menu_setting"
