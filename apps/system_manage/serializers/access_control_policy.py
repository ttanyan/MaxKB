# coding=utf-8
"""
    @project: MaxKB
    @Author：TanLianWang
    @file： access_control_policy.py
    @date：2026/4/1
    @desc: 接入控制策略序列化
"""
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from common.exception.app_exception import AppApiException
from system_manage.models import AccessControlPolicy, AccessControlPolicyApplicationRecord


def _normalize_string_list(value):
    normalized = []
    seen = set()
    for item in value or []:
        text = str(item).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        normalized.append(text)
    return normalized


class AccessControlPolicySerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    name = serializers.CharField(required=True, max_length=128)
    description = serializers.CharField(required=False, allow_blank=True, default='')
    enabled = serializers.BooleanField(required=False, default=True)
    access_time_enabled = serializers.BooleanField(required=False, default=False)
    access_start_time = serializers.TimeField(required=False, allow_null=True)
    access_end_time = serializers.TimeField(required=False, allow_null=True)
    allowed_weekdays = serializers.ListField(child=serializers.IntegerField(min_value=1, max_value=7), required=False)
    allowed_device_types = serializers.ListField(child=serializers.CharField(), required=False)
    allowed_regions = serializers.ListField(child=serializers.CharField(), required=False)
    effect_start_time = serializers.DateTimeField(required=False, allow_null=True)
    effect_end_time = serializers.DateTimeField(required=False, allow_null=True)
    application_count = serializers.IntegerField(required=False)
    last_applied_time = serializers.DateTimeField(required=False, allow_null=True)
    create_time = serializers.DateTimeField(required=False)
    update_time = serializers.DateTimeField(required=False)
    content = serializers.CharField(required=False)

    @staticmethod
    def _build_content(data):
        segments = []
        if data.get('access_time_enabled') and data.get('access_start_time') and data.get('access_end_time'):
            weekdays = data.get('allowed_weekdays') or []
            weekday_text = '、'.join([f'周{["一", "二", "三", "四", "五", "六", "日"][int(item) - 1]}' for item in weekdays]) if weekdays else '每日'
            segments.append(f'{weekday_text} {data.get("access_start_time")} - {data.get("access_end_time")}')
        else:
            segments.append('不限访问时段')
        device_types = data.get('allowed_device_types') or []
        segments.append(f'设备类型：{"、".join(device_types) if device_types else "不限"}')
        regions = data.get('allowed_regions') or []
        segments.append(f'接入区域：{"、".join(regions) if regions else "不限"}')
        return '；'.join(segments)

    @staticmethod
    def to_representation_from_instance(instance: AccessControlPolicy):
        data = {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'enabled': instance.enabled,
            'access_time_enabled': instance.access_time_enabled,
            'access_start_time': instance.access_start_time.strftime('%H:%M:%S') if instance.access_start_time else None,
            'access_end_time': instance.access_end_time.strftime('%H:%M:%S') if instance.access_end_time else None,
            'allowed_weekdays': instance.allowed_weekdays or [],
            'allowed_device_types': instance.allowed_device_types or [],
            'allowed_regions': instance.allowed_regions or [],
            'effect_start_time': instance.effect_start_time.isoformat() if instance.effect_start_time else None,
            'effect_end_time': instance.effect_end_time.isoformat() if instance.effect_end_time else None,
            'application_count': instance.application_count,
            'last_applied_time': instance.last_applied_time.isoformat() if instance.last_applied_time else None,
            'create_time': instance.create_time.isoformat() if instance.create_time else None,
            'update_time': instance.update_time.isoformat() if instance.update_time else None,
        }
        data['content'] = AccessControlPolicySerializer._build_content(data)
        return data

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise AppApiException(500, '策略名称不能为空')
        queryset = AccessControlPolicy.objects.filter(name=value)
        if self.instance is not None:
            queryset = queryset.exclude(id=self.instance.id)
        if queryset.exists():
            raise AppApiException(500, '策略名称已存在')
        return value

    def validate_allowed_weekdays(self, value):
        return sorted(set(value or []))

    def validate_allowed_device_types(self, value):
        return _normalize_string_list(value)

    def validate_allowed_regions(self, value):
        return _normalize_string_list(value)

    def validate(self, attrs):
        access_time_enabled = attrs.get('access_time_enabled', getattr(self.instance, 'access_time_enabled', False))
        access_start_time = attrs.get('access_start_time', getattr(self.instance, 'access_start_time', None))
        access_end_time = attrs.get('access_end_time', getattr(self.instance, 'access_end_time', None))
        effect_start_time = attrs.get('effect_start_time', getattr(self.instance, 'effect_start_time', None))
        effect_end_time = attrs.get('effect_end_time', getattr(self.instance, 'effect_end_time', None))

        if access_time_enabled and (access_start_time is None or access_end_time is None):
            raise AppApiException(500, '启用访问时段限制后，必须设置开始和结束时间')
        if access_start_time and access_end_time and access_start_time >= access_end_time:
            raise AppApiException(500, '访问结束时间必须晚于开始时间')
        if effect_start_time and effect_end_time and effect_start_time >= effect_end_time:
            raise AppApiException(500, '生效结束时间必须晚于开始时间')
        return attrs

    @transaction.atomic
    def save(self, **kwargs):
        self.is_valid(raise_exception=True)
        validated_data = self.validated_data
        if self.instance is None:
            instance = AccessControlPolicy.objects.create(**validated_data)
        else:
            instance = self.instance
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
        return self.to_representation_from_instance(instance)

    @staticmethod
    def list(name='', enabled=None):
        queryset = AccessControlPolicy.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name.strip())
        if enabled in ['true', 'false']:
            queryset = queryset.filter(enabled=(enabled == 'true'))
        return [AccessControlPolicySerializer.to_representation_from_instance(item) for item in queryset]

    @staticmethod
    def get_one(policy_id):
        instance = AccessControlPolicy.objects.filter(id=policy_id).first()
        if instance is None:
            raise AppApiException(500, '接入控制策略不存在')
        return instance


class AccessControlPolicyApplySerializer(serializers.Serializer):
    target_type = serializers.ChoiceField(choices=AccessControlPolicyApplicationRecord.TargetType.choices)
    target_name = serializers.CharField(required=True, max_length=128)
    target_identifier = serializers.CharField(required=False, allow_blank=True, default='', max_length=128)
    remark = serializers.CharField(required=False, allow_blank=True, default='')

    @transaction.atomic
    def save(self, policy: AccessControlPolicy, operator):
        self.is_valid(raise_exception=True)
        validated_data = self.validated_data
        AccessControlPolicyApplicationRecord.objects.create(
            policy=policy,
            policy_name=policy.name,
            target_type=validated_data.get('target_type'),
            target_name=validated_data.get('target_name').strip(),
            target_identifier=validated_data.get('target_identifier', '').strip(),
            remark=validated_data.get('remark', '').strip(),
            operator=operator,
            operator_name=getattr(operator, 'nick_name', '') or getattr(operator, 'username', ''),
        )
        policy.application_count = (policy.application_count or 0) + 1
        policy.last_applied_time = timezone.now()
        policy.save(update_fields=['application_count', 'last_applied_time', 'update_time'])
        return {'policy_id': str(policy.id), 'target_name': validated_data.get('target_name').strip()}


class AccessControlPolicyApplicationRecordSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    policy_id = serializers.UUIDField(required=False, allow_null=True)
    policy_name = serializers.CharField(required=False)
    target_type = serializers.CharField(required=False)
    target_name = serializers.CharField(required=False)
    target_identifier = serializers.CharField(required=False)
    remark = serializers.CharField(required=False)
    operator_name = serializers.CharField(required=False)
    apply_time = serializers.DateTimeField(required=False)

    @staticmethod
    def list(policy_name='', target_name=''):
        queryset = AccessControlPolicyApplicationRecord.objects.all()
        if policy_name:
            queryset = queryset.filter(policy_name__icontains=policy_name.strip())
        if target_name:
            queryset = queryset.filter(Q(target_name__icontains=target_name.strip()) | Q(target_identifier__icontains=target_name.strip()))
        records = []
        for item in queryset:
            records.append({
                'id': item.id,
                'policy_id': item.policy_id,
                'policy_name': item.policy_name,
                'target_type': item.target_type,
                'target_name': item.target_name,
                'target_identifier': item.target_identifier,
                'remark': item.remark,
                'operator_name': item.operator_name,
                'apply_time': item.create_time.isoformat() if item.create_time else None,
            })
        return records
