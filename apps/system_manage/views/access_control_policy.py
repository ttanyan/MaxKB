# coding=utf-8
"""
    @project: MaxKB
    @Author：TanLianWang
    @file： access_control_policy.py
    @date：2026/4/1
    @desc: 接入控制策略视图
"""
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from common.auth import TokenAuth
from common.auth.authentication import has_permissions
from common.constants.permission_constants import PermissionConstants, RoleConstants
from common.log.log import log
from common.result import result
from system_manage.serializers.access_control_policy import (
    AccessControlPolicySerializer,
    AccessControlPolicyApplySerializer,
    AccessControlPolicyApplicationRecordSerializer,
)


def get_access_control_policy_details(request):
    return {
        'path': request.path,
        'body': request.data,
        'query': request.query_params,
    }


class AccessControlPolicyView(APIView):
    authentication_classes = [TokenAuth]

    @extend_schema(tags=['Access Control Policy'])
    @has_permissions(PermissionConstants.USER_READ, RoleConstants.ADMIN)
    def get(self, request: Request):
        return result.success(
            AccessControlPolicySerializer.list(
                name=request.query_params.get('name', ''),
                enabled=request.query_params.get('enabled'),
            )
        )

    @extend_schema(tags=['Access Control Policy'])
    @log(menu='Policy management', operate='Create access control policy', get_details=get_access_control_policy_details)
    @has_permissions(PermissionConstants.USER_EDIT, RoleConstants.ADMIN)
    def post(self, request: Request):
        return result.success(AccessControlPolicySerializer(data=request.data).save())


class AccessControlPolicyDetailView(APIView):
    authentication_classes = [TokenAuth]

    @extend_schema(tags=['Access Control Policy'])
    @has_permissions(PermissionConstants.USER_READ, RoleConstants.ADMIN)
    def get(self, request: Request, policy_id):
        return result.success(
            AccessControlPolicySerializer.to_representation_from_instance(
                AccessControlPolicySerializer.get_one(policy_id)
            )
        )

    @extend_schema(tags=['Access Control Policy'])
    @log(menu='Policy management', operate='Update access control policy', get_details=get_access_control_policy_details)
    @has_permissions(PermissionConstants.USER_EDIT, RoleConstants.ADMIN)
    def put(self, request: Request, policy_id):
        instance = AccessControlPolicySerializer.get_one(policy_id)
        return result.success(AccessControlPolicySerializer(instance=instance, data=request.data).save())

    @extend_schema(tags=['Access Control Policy'])
    @log(menu='Policy management', operate='Delete access control policy', get_details=get_access_control_policy_details)
    @has_permissions(PermissionConstants.USER_EDIT, RoleConstants.ADMIN)
    def delete(self, request: Request, policy_id):
        instance = AccessControlPolicySerializer.get_one(policy_id)
        instance.delete()
        return result.success(True)


class AccessControlPolicyApplyView(APIView):
    authentication_classes = [TokenAuth]

    @extend_schema(tags=['Access Control Policy'])
    @log(menu='Policy management', operate='Apply access control policy', get_details=get_access_control_policy_details)
    @has_permissions(PermissionConstants.USER_EDIT, RoleConstants.ADMIN)
    def post(self, request: Request, policy_id):
        policy = AccessControlPolicySerializer.get_one(policy_id)
        serializer = AccessControlPolicyApplySerializer(data=request.data)
        return result.success(serializer.save(policy=policy, operator=request.user))


class AccessControlPolicyApplicationRecordView(APIView):
    authentication_classes = [TokenAuth]

    @extend_schema(tags=['Access Control Policy'])
    @has_permissions(PermissionConstants.USER_READ, RoleConstants.ADMIN)
    def get(self, request: Request):
        return result.success(
            AccessControlPolicyApplicationRecordSerializer.list(
                policy_name=request.query_params.get('policy_name', ''),
                target_name=request.query_params.get('target_name', ''),
            )
        )
