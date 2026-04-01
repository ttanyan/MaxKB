<template>
  <div class="policy-page p-16-24">
    <el-breadcrumb separator-icon="ArrowRight" class="mb-16">
      <el-breadcrumb-item>{{ t('views.system.subTitle') }}</el-breadcrumb-item>
      <el-breadcrumb-item>
        <h5 class="ml-4 color-text-primary">{{ t('views.system.policy.title') }}</h5>
      </el-breadcrumb-item>
    </el-breadcrumb>

    <el-card shadow="never" class="policy-page__card">
      <el-tabs v-model="activeTab">
        <el-tab-pane :label="t('views.system.policy.configTab')" name="policy">
          <div class="policy-page__toolbar mb-16">
            <div class="policy-page__filters">
              <el-input
                v-model="policyQuery.name"
                clearable
                :placeholder="t('views.system.policy.searchPolicyPlaceholder')"
                style="width: 240px"
                @keyup.enter="loadPolicies"
              />
              <el-select v-model="policyQuery.enabled" clearable style="width: 180px">
                <el-option :label="t('views.system.policy.allStatus')" value="" />
                <el-option :label="t('common.status.enabled')" value="true" />
                <el-option :label="t('common.status.disabled')" value="false" />
              </el-select>
              <el-button @click="loadPolicies">{{ t('common.search') }}</el-button>
              <el-button @click="resetPolicyFilters">{{ t('common.clear') }}</el-button>
            </div>
            <el-button type="primary" @click="openPolicyDialog()">
              {{ t('views.system.policy.createPolicy') }}
            </el-button>
          </div>

          <el-table :data="policyList" border v-loading="policyLoading">
            <el-table-column prop="name" :label="t('views.system.policy.policyName')" min-width="180" />
            <el-table-column prop="content" :label="t('views.system.policy.policyContent')" min-width="360" show-overflow-tooltip />
            <el-table-column :label="t('views.system.policy.effectiveTime')" min-width="240">
              <template #default="{ row }">
                {{ formatEffectiveTime(row.effect_start_time, row.effect_end_time) }}
              </template>
            </el-table-column>
            <el-table-column prop="application_count" :label="t('views.system.policy.applicationCount')" width="110" align="center" />
            <el-table-column :label="t('common.status.label')" width="110" align="center">
              <template #default="{ row }">
                <el-tag :type="row.enabled ? 'success' : 'info'" effect="light">
                  {{ row.enabled ? t('common.status.enabled') : t('common.status.disabled') }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column :label="t('views.system.policy.lastAppliedTime')" min-width="180">
              <template #default="{ row }">
                {{ formatDateTime(row.last_applied_time) }}
              </template>
            </el-table-column>
            <el-table-column :label="t('common.operation')" fixed="right" width="220">
              <template #default="{ row }">
                <el-button link type="primary" @click="openApplyDialog(row)">
                  {{ t('views.system.policy.applyPolicy') }}
                </el-button>
                <el-button link type="primary" @click="openPolicyDialog(row)">
                  {{ t('common.edit') }}
                </el-button>
                <el-button link type="danger" @click="removePolicy(row)">
                  {{ t('common.delete') }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane :label="t('views.system.policy.recordTab')" name="record">
          <div class="policy-page__toolbar mb-16">
            <div class="policy-page__filters">
              <el-input
                v-model="recordQuery.policy_name"
                clearable
                :placeholder="t('views.system.policy.searchRecordPolicyPlaceholder')"
                style="width: 240px"
                @keyup.enter="loadRecords"
              />
              <el-input
                v-model="recordQuery.target_name"
                clearable
                :placeholder="t('views.system.policy.searchRecordTargetPlaceholder')"
                style="width: 240px"
                @keyup.enter="loadRecords"
              />
              <el-button @click="loadRecords">{{ t('common.search') }}</el-button>
              <el-button @click="resetRecordFilters">{{ t('common.clear') }}</el-button>
            </div>
          </div>

          <el-table :data="recordList" border v-loading="recordLoading">
            <el-table-column prop="policy_name" :label="t('views.system.policy.policyName')" min-width="180" />
            <el-table-column :label="t('views.system.policy.targetType')" width="120" align="center">
              <template #default="{ row }">
                {{ targetTypeLabelMap[row.target_type] || row.target_type }}
              </template>
            </el-table-column>
            <el-table-column prop="target_name" :label="t('views.system.policy.targetName')" min-width="180" />
            <el-table-column prop="target_identifier" :label="t('views.system.policy.targetIdentifier')" min-width="160" />
            <el-table-column prop="operator_name" :label="t('views.system.policy.operator')" width="140" />
            <el-table-column :label="t('views.system.policy.applyTime')" min-width="180">
              <template #default="{ row }">
                {{ formatDateTime(row.apply_time) }}
              </template>
            </el-table-column>
            <el-table-column prop="remark" :label="t('views.system.policy.remark')" min-width="220" show-overflow-tooltip />
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog
      v-model="policyDialogVisible"
      :title="editingPolicyId ? t('views.system.policy.editPolicy') : t('views.system.policy.createPolicy')"
      width="760px"
      class="policy-dialog"
      destroy-on-close
    >
      <el-form
        ref="policyFormRef"
        :model="policyForm"
        :rules="policyRules"
        label-position="top"
        class="policy-dialog__form"
      >
        <div class="policy-dialog__grid">
          <div class="policy-dialog__col">
            <el-form-item :label="t('views.system.policy.policyName')" prop="name">
              <el-input v-model="policyForm.name" maxlength="128" />
            </el-form-item>
          </div>

          <div class="policy-dialog__col">
            <el-form-item :label="t('common.status.label')" prop="enabled">
              <el-switch v-model="policyForm.enabled" />
            </el-form-item>
          </div>

          <div class="policy-dialog__col policy-dialog__col--full">
            <el-form-item :label="t('views.system.policy.description')" prop="description">
              <el-input v-model="policyForm.description" type="textarea" :rows="3" maxlength="500" show-word-limit />
            </el-form-item>
          </div>

          <div class="policy-dialog__col">
            <el-form-item :label="t('views.system.policy.accessTimeLimit')" prop="access_time_enabled">
              <el-switch v-model="policyForm.access_time_enabled" />
            </el-form-item>
          </div>

          <template v-if="policyForm.access_time_enabled">
            <div class="policy-dialog__col">
              <el-form-item :label="t('views.system.policy.weekdays')" prop="allowed_weekdays">
                <el-checkbox-group v-model="policyForm.allowed_weekdays" class="policy-dialog__weekdays">
                  <el-checkbox v-for="item in weekdayOptions" :key="item.value" :label="item.value">
                    {{ item.label }}
                  </el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </div>
            <div class="policy-dialog__col policy-dialog__col--full">
              <el-form-item :label="t('views.system.policy.accessPeriod')">
                <div class="policy-dialog__range">
                  <el-time-picker
                    v-model="policyForm.access_start_time"
                    value-format="HH:mm:ss"
                    :placeholder="t('views.system.policy.startTime')"
                  />
                  <span class="policy-page__separator">-</span>
                  <el-time-picker
                    v-model="policyForm.access_end_time"
                    value-format="HH:mm:ss"
                    :placeholder="t('views.system.policy.endTime')"
                  />
                </div>
              </el-form-item>
            </div>
          </template>

          <div class="policy-dialog__col policy-dialog__col--full">
            <el-form-item :label="t('views.system.policy.deviceTypes')" prop="allowed_device_types">
              <el-select
                v-model="policyForm.allowed_device_types"
                multiple
                filterable
                allow-create
                default-first-option
              >
                <el-option v-for="item in deviceTypeOptions" :key="item" :label="item" :value="item" />
              </el-select>
            </el-form-item>
          </div>

          <div class="policy-dialog__col policy-dialog__col--full">
            <el-form-item :label="t('views.system.policy.regions')" prop="allowed_regions">
              <el-select
                v-model="policyForm.allowed_regions"
                multiple
                filterable
                allow-create
                default-first-option
              >
                <el-option v-for="item in regionOptions" :key="item" :label="item" :value="item" />
              </el-select>
            </el-form-item>
          </div>

          <div class="policy-dialog__col policy-dialog__col--full">
            <el-form-item :label="t('views.system.policy.effectiveTime')">
              <div class="policy-dialog__range">
                <el-date-picker
                  v-model="policyForm.effect_start_time"
                  type="datetime"
                  value-format="YYYY-MM-DDTHH:mm:ss"
                  :placeholder="t('views.system.policy.startTime')"
                />
                <span class="policy-page__separator">-</span>
                <el-date-picker
                  v-model="policyForm.effect_end_time"
                  type="datetime"
                  value-format="YYYY-MM-DDTHH:mm:ss"
                  :placeholder="t('views.system.policy.endTime')"
                />
              </div>
            </el-form-item>
          </div>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="policyDialogVisible = false">{{ t('common.cancel') }}</el-button>
        <el-button type="primary" :loading="saveLoading" @click="submitPolicy">
          {{ t('common.save') }}
        </el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="applyDialogVisible"
      :title="t('views.system.policy.applyPolicy')"
      width="560px"
      class="policy-dialog"
      destroy-on-close
    >
      <el-form
        ref="applyFormRef"
        :model="applyForm"
        :rules="applyRules"
        label-position="top"
        class="policy-dialog__form"
      >
        <div class="policy-dialog__grid">
          <div class="policy-dialog__col policy-dialog__col--full">
            <el-form-item :label="t('views.system.policy.selectedPolicy')">
              <el-input :model-value="applyPolicyName" disabled />
            </el-form-item>
          </div>

          <div class="policy-dialog__col policy-dialog__col--full">
            <el-form-item :label="t('views.system.policy.targetType')" prop="target_type">
              <el-radio-group v-model="applyForm.target_type" class="policy-dialog__radio-group">
                <el-radio-button label="DEVICE">{{ t('views.system.policy.device') }}</el-radio-button>
                <el-radio-button label="SERVICE">{{ t('views.system.policy.service') }}</el-radio-button>
              </el-radio-group>
            </el-form-item>
          </div>

          <div class="policy-dialog__col policy-dialog__col--full">
            <el-form-item :label="t('views.system.policy.targetName')" prop="target_name">
              <el-input v-model="applyForm.target_name" />
            </el-form-item>
          </div>

          <div class="policy-dialog__col policy-dialog__col--full">
            <el-form-item :label="t('views.system.policy.targetIdentifier')" prop="target_identifier">
              <el-input v-model="applyForm.target_identifier" />
            </el-form-item>
          </div>

          <div class="policy-dialog__col policy-dialog__col--full">
            <el-form-item :label="t('views.system.policy.remark')" prop="remark">
              <el-input v-model="applyForm.remark" type="textarea" :rows="3" maxlength="500" show-word-limit />
            </el-form-item>
          </div>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="applyDialogVisible = false">{{ t('common.cancel') }}</el-button>
        <el-button type="primary" :loading="applyLoading" @click="submitApply">
          {{ t('common.confirm') }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import accessControlPolicyApi from '@/api/system-settings/access-control-policy'
import { MsgConfirm, MsgSuccess } from '@/utils/message'
import { t } from '@/locales'

const activeTab = ref('policy')
const policyLoading = ref(false)
const recordLoading = ref(false)
const saveLoading = ref(false)
const applyLoading = ref(false)
const policyDialogVisible = ref(false)
const applyDialogVisible = ref(false)
const editingPolicyId = ref('')
const applyingPolicyId = ref('')
const applyPolicyName = ref('')

const policyFormRef = ref<FormInstance>()
const applyFormRef = ref<FormInstance>()

const policyList = ref<any[]>([])
const recordList = ref<any[]>([])

const policyQuery = reactive({
  name: '',
  enabled: '',
})

const recordQuery = reactive({
  policy_name: '',
  target_name: '',
})

const policyForm = reactive({
  name: '',
  description: '',
  enabled: true,
  access_time_enabled: false,
  access_start_time: '',
  access_end_time: '',
  allowed_weekdays: [] as number[],
  allowed_device_types: [] as string[],
  allowed_regions: [] as string[],
  effect_start_time: '',
  effect_end_time: '',
})

const applyForm = reactive({
  target_type: 'DEVICE',
  target_name: '',
  target_identifier: '',
  remark: '',
})

const weekdayOptions = [
  { label: t('views.system.policy.monday'), value: 1 },
  { label: t('views.system.policy.tuesday'), value: 2 },
  { label: t('views.system.policy.wednesday'), value: 3 },
  { label: t('views.system.policy.thursday'), value: 4 },
  { label: t('views.system.policy.friday'), value: 5 },
  { label: t('views.system.policy.saturday'), value: 6 },
  { label: t('views.system.policy.sunday'), value: 7 },
]

const deviceTypeOptions = ['摄像头', '门禁设备', '工控终端', '移动终端', '服务器']
const regionOptions = ['北京', '上海', '广州', '深圳', '成都', '西安']

const targetTypeLabelMap: Record<string, string> = {
  DEVICE: t('views.system.policy.device'),
  SERVICE: t('views.system.policy.service'),
}

const policyRules = computed<FormRules>(() => ({
  name: [{ required: true, message: t('views.system.policy.policyNameRequired'), trigger: 'blur' }],
}))

const applyRules = computed<FormRules>(() => ({
  target_type: [{ required: true, message: t('views.system.policy.targetTypeRequired'), trigger: 'change' }],
  target_name: [{ required: true, message: t('views.system.policy.targetNameRequired'), trigger: 'blur' }],
}))

function resetPolicyForm() {
  editingPolicyId.value = ''
  policyForm.name = ''
  policyForm.description = ''
  policyForm.enabled = true
  policyForm.access_time_enabled = false
  policyForm.access_start_time = ''
  policyForm.access_end_time = ''
  policyForm.allowed_weekdays = []
  policyForm.allowed_device_types = []
  policyForm.allowed_regions = []
  policyForm.effect_start_time = ''
  policyForm.effect_end_time = ''
}

function resetApplyForm() {
  applyingPolicyId.value = ''
  applyPolicyName.value = ''
  applyForm.target_type = 'DEVICE'
  applyForm.target_name = ''
  applyForm.target_identifier = ''
  applyForm.remark = ''
}

function normalizeDateTimeValue(value?: string | null) {
  if (!value) return ''
  return value.includes('.') ? value.split('.')[0] : value.replace(/Z$/, '')
}

function formatDateTime(value?: string | null) {
  if (!value) return '-'
  return normalizeDateTimeValue(value).replace('T', ' ')
}

function formatEffectiveTime(start?: string | null, end?: string | null) {
  if (!start && !end) return t('views.system.policy.unlimited')
  return `${formatDateTime(start)} ~ ${formatDateTime(end)}`
}

async function loadPolicies() {
  const response = await accessControlPolicyApi.getPolicyList(
    { ...policyQuery, enabled: policyQuery.enabled || undefined },
    policyLoading,
  )
  policyList.value = response.data || []
}

async function loadRecords() {
  const response = await accessControlPolicyApi.getApplicationRecordList(recordQuery, recordLoading)
  recordList.value = response.data || []
}

function resetPolicyFilters() {
  policyQuery.name = ''
  policyQuery.enabled = ''
  loadPolicies()
}

function resetRecordFilters() {
  recordQuery.policy_name = ''
  recordQuery.target_name = ''
  loadRecords()
}

function openPolicyDialog(row?: any) {
  resetPolicyForm()
  policyDialogVisible.value = true
  if (!row) return
  editingPolicyId.value = row.id
  policyForm.name = row.name || ''
  policyForm.description = row.description || ''
  policyForm.enabled = row.enabled ?? true
  policyForm.access_time_enabled = row.access_time_enabled ?? false
  policyForm.access_start_time = row.access_start_time || ''
  policyForm.access_end_time = row.access_end_time || ''
  policyForm.allowed_weekdays = row.allowed_weekdays || []
  policyForm.allowed_device_types = row.allowed_device_types || []
  policyForm.allowed_regions = row.allowed_regions || []
  policyForm.effect_start_time = normalizeDateTimeValue(row.effect_start_time)
  policyForm.effect_end_time = normalizeDateTimeValue(row.effect_end_time)
}

async function submitPolicy() {
  await policyFormRef.value?.validate()
  const payload = {
    ...policyForm,
    access_start_time: policyForm.access_time_enabled ? policyForm.access_start_time || null : null,
    access_end_time: policyForm.access_time_enabled ? policyForm.access_end_time || null : null,
    allowed_weekdays: policyForm.access_time_enabled ? policyForm.allowed_weekdays : [],
    effect_start_time: policyForm.effect_start_time || null,
    effect_end_time: policyForm.effect_end_time || null,
  }
  if (editingPolicyId.value) {
    await accessControlPolicyApi.updatePolicy(editingPolicyId.value, payload, saveLoading)
  } else {
    await accessControlPolicyApi.createPolicy(payload, saveLoading)
  }
  MsgSuccess(t('common.saveSuccess'))
  policyDialogVisible.value = false
  loadPolicies()
}

async function removePolicy(row: any) {
  try {
    await MsgConfirm(t('common.delete'), t('views.system.policy.deletePolicyTip', { name: row.name }))
  } catch (error) {
    return
  }
  await accessControlPolicyApi.deletePolicy(row.id)
  MsgSuccess(t('common.deleteSuccess'))
  loadPolicies()
  loadRecords()
}

function openApplyDialog(row: any) {
  resetApplyForm()
  applyingPolicyId.value = row.id
  applyPolicyName.value = row.name
  applyDialogVisible.value = true
}

async function submitApply() {
  await applyFormRef.value?.validate()
  await accessControlPolicyApi.applyPolicy(applyingPolicyId.value, applyForm, applyLoading)
  MsgSuccess(t('views.system.policy.applySuccess'))
  applyDialogVisible.value = false
  activeTab.value = 'record'
  loadPolicies()
  loadRecords()
}

onMounted(async () => {
  await Promise.all([loadPolicies(), loadRecords()])
})
</script>

<style lang="scss" scoped>
.policy-page {
  &__card {
    border-radius: 12px;
  }

  &__toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
  }

  &__filters {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }

  &__separator {
    margin: 0 12px;
    color: var(--el-text-color-secondary);
  }
}

:deep(.policy-dialog) {
  .el-dialog__body {
    padding-top: 20px;
  }
}

.policy-dialog {
  &__form {
    :deep(.el-form-item) {
      margin-bottom: 20px;
    }

    :deep(.el-form-item__label) {
      padding-bottom: 8px;
      line-height: 20px;
      font-weight: 500;
    }

    :deep(.el-form-item__content) {
      min-width: 0;
      width: 100%;
    }

    :deep(.el-input),
    :deep(.el-textarea),
    :deep(.el-select),
    :deep(.el-date-editor.el-input),
    :deep(.el-date-editor.el-input__wrapper),
    :deep(.el-date-editor.el-range-editor) {
      width: 100%;
    }
  }

  &__grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0 16px;
  }

  &__col {
    min-width: 0;
  }

  &__col--full {
    grid-column: 1 / -1;
  }

  &__range {
    display: flex;
    align-items: center;
    width: 100%;

    :deep(.el-date-editor),
    :deep(.el-input),
    :deep(.el-select) {
      flex: 1;
      width: 100%;
    }
  }

  &__weekdays {
    display: flex;
    flex-wrap: wrap;
    gap: 8px 16px;
  }

  &__radio-group {
    display: inline-flex;
    flex-wrap: wrap;
  }
}

@media (max-width: 900px) {
  .policy-dialog {
    &__grid {
      grid-template-columns: minmax(0, 1fr);
    }

    &__range {
      flex-direction: column;
      align-items: stretch;

      .policy-page__separator {
        margin: 8px 0;
        text-align: center;
      }
    }
  }
}
</style>
