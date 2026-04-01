# coding=utf-8
"""
    @project: MaxKB
    @Author：TanLianWang
    @file： access_control_policy.py
    @date：2026/4/1
    @desc: 接入控制策略
"""
import uuid_utils.compat as uuid

from django.db import models

from common.mixins.app_model_mixin import AppModelMixin
from users.models import User


class AccessControlPolicy(AppModelMixin):
    """
    接入控制策略
    """

    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="主键id")
    name = models.CharField(max_length=128, unique=True, verbose_name="策略名称")
    description = models.TextField(blank=True, default="", verbose_name="策略描述")
    enabled = models.BooleanField(default=True, verbose_name="是否启用")
    access_time_enabled = models.BooleanField(default=False, verbose_name="是否限制访问时段")
    access_start_time = models.TimeField(null=True, blank=True, verbose_name="访问开始时间")
    access_end_time = models.TimeField(null=True, blank=True, verbose_name="访问结束时间")
    allowed_weekdays = models.JSONField(default=list, verbose_name="允许访问星期")
    allowed_device_types = models.JSONField(default=list, verbose_name="允许接入设备类型")
    allowed_regions = models.JSONField(default=list, verbose_name="允许接入区域")
    effect_start_time = models.DateTimeField(null=True, blank=True, verbose_name="生效开始时间")
    effect_end_time = models.DateTimeField(null=True, blank=True, verbose_name="生效结束时间")
    application_count = models.PositiveIntegerField(default=0, verbose_name="应用次数")
    last_applied_time = models.DateTimeField(null=True, blank=True, verbose_name="最近应用时间")

    class Meta:
        db_table = "access_control_policy"
        ordering = ['-update_time', '-create_time']


class AccessControlPolicyApplicationRecord(AppModelMixin):
    """
    接入控制策略应用记录
    """

    class TargetType(models.TextChoices):
        DEVICE = "DEVICE", "设备"
        SERVICE = "SERVICE", "服务"

    id = models.UUIDField(primary_key=True, max_length=128, default=uuid.uuid7, editable=False, verbose_name="主键id")
    policy = models.ForeignKey(
        AccessControlPolicy,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='application_records',
        verbose_name="策略",
    )
    policy_name = models.CharField(max_length=128, verbose_name="策略名称快照")
    target_type = models.CharField(max_length=32, choices=TargetType.choices, verbose_name="应用对象类型")
    target_name = models.CharField(max_length=128, verbose_name="应用对象名称")
    target_identifier = models.CharField(max_length=128, blank=True, default="", verbose_name="应用对象标识")
    remark = models.TextField(blank=True, default="", verbose_name="备注")
    operator = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="操作人",
    )
    operator_name = models.CharField(max_length=128, blank=True, default="", verbose_name="操作人名称")

    class Meta:
        db_table = "access_control_policy_application_record"
        ordering = ['-create_time']
