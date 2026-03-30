<template>
  <div class="p-16-24">
    <h2 class="mb-16">{{ $t('common.setting') }}</h2>
    <el-card style="--el-card-padding: 0">
      <div class="knowledge-setting main-calc-height">
        <el-scrollbar>
          <div class="p-24" v-loading="loading">
            <h4 class="title-decoration-1 mb-16">
              {{ $t('common.info') }}
            </h4>
            <BaseForm ref="BaseFormRef" :data="detail" :apiType="apiType"/>
            <el-card shadow="never" class="mb-16 w-full layout-bg">
              <el-descriptions :column="3" border class="creator-info-descriptions">
                <el-descriptions-item :label="$t('common.creator')" class="creator-info-item">
                  <el-select v-model="selectedCreator" placeholder="请选择创建者" v-if="!route.path.includes('share/') && permissionPrecise.edit(id)" class="creator-select">
                    <el-option v-for="user in user_options" :key="user.id" :label="user.nick_name" :value="user.id" />
                  </el-select>
                  <span v-else class="creator-text">{{ detail?.nick_name ? i18n_name(detail.nick_name) : detail?.create_user || $t('common.unknown') }}</span>
                </el-descriptions-item>
                <el-descriptions-item :label="$t('common.createTime')" class="creator-info-item">
                  <span class="creator-text">{{ detail?.create_time ? new Date(detail.create_time).toLocaleString() : $t('common.unknown') }}</span>
                </el-descriptions-item>
                <el-descriptions-item :label="$t('common.updateTime')" class="creator-info-item">
                  <span class="creator-text">{{ detail?.update_time ? new Date(detail.update_time).toLocaleString() : $t('common.unknown') }}</span>
                </el-descriptions-item>
              </el-descriptions>
            </el-card>

            <el-form
              ref="webFormRef"
              :rules="rules"
              :model="form"
              label-position="top"
              require-asterisk-position="right"
            >
              <el-form-item :label="$t('views.knowledge.knowledgeType.label')" required>
                <el-card
                  shadow="never"
                  class="mb-8 w-full layout-bg"
                  style="line-height: 22px"
                  v-if="detail?.type === 0"
                >
                  <div class="flex align-center">
                    <el-avatar class="mr-8 avatar-blue" shape="square" :size="32">
                      <img src="@/assets/knowledge/icon_document.svg" style="width: 58%" alt=""/>
                    </el-avatar>
                    <div>
                      <div>{{ $t('views.knowledge.knowledgeType.generalKnowledge') }}</div>
                      <el-text type="info"
                      >{{ $t('views.knowledge.knowledgeType.generalInfo') }}
                      </el-text>
                    </div>
                  </div>
                </el-card>
                <el-card
                  shadow="never"
                  class="mb-8 w-full layout-bg"
                  style="line-height: 22px"
                  v-if="detail?.type === 1"
                >
                  <div class="flex align-center">
                    <el-avatar class="mr-8 avatar-purple" shape="square" :size="32">
                      <img src="@/assets/knowledge/icon_web.svg" style="width: 58%" alt=""/>
                    </el-avatar>
                    <div>
                      <div>{{ $t('views.knowledge.knowledgeType.webKnowledge') }}</div>
                      <el-text type="info">
                        {{ $t('views.knowledge.knowledgeType.webInfo') }}
                      </el-text>
                    </div>
                  </div>
                </el-card>
                <el-card
                  shadow="never"
                  class="mb-8 w-full layout-bg"
                  style="line-height: 22px"
                  v-if="detail?.type === 2"
                >
                  <div class="flex align-center">
                    <el-avatar shape="square" :size="32" style="background: none">
                      <img src="@/assets/knowledge/logo_lark.svg" style="width: 100%" alt=""/>
                    </el-avatar>
                    <div>
                      <p>
                        <el-text>{{ $t('views.knowledge.knowledgeType.larkKnowledge') }}</el-text>
                      </p>
                      <el-text type="info"
                      >{{ $t('views.knowledge.knowledgeType.larkInfo') }}
                      </el-text>
                    </div>
                  </div>
                </el-card>
              </el-form-item>
              <el-form-item
                :label="$t('views.knowledge.form.source_url.label')"
                prop="source_url"
                v-if="detail?.type === 1"
              >
                <el-input
                  v-model="form.source_url"
                  :placeholder="$t('views.knowledge.form.source_url.placeholder')"
                  @blur="form.source_url = form.source_url.trim()"
                />
              </el-form-item>
              <el-form-item
                :label="$t('views.knowledge.form.selector.label')"
                v-if="detail?.type === 1"
              >
                <el-input
                  v-model="form.selector"
                  :placeholder="$t('views.knowledge.form.selector.placeholder')"
                  @blur="form.selector = form.selector.trim()"
                />
              </el-form-item>
              <el-form-item label="App ID" prop="app_id" v-if="detail?.type === 2">
                <el-input
                  v-model="form.app_id"
                  :placeholder="
                    $t('views.application.applicationAccess.larkSetting.appIdPlaceholder')
                  "
                />
              </el-form-item>
              <el-form-item label="App Secret" prop="app_id" v-if="detail?.type === 2">
                <el-input
                  v-model="form.app_secret"
                  type="password"
                  show-password
                  :placeholder="
                    $t('views.application.applicationAccess.larkSetting.appSecretPlaceholder')
                  "
                />
              </el-form-item>
              <el-form-item label="Folder Token" prop="folder_token" v-if="detail?.type === 2">
                <el-input
                  v-model="form.folder_token"
                  :placeholder="
                    $t('views.application.applicationAccess.larkSetting.folderTokenPlaceholder')
                  "
                />
              </el-form-item>

              <div v-if="detail?.type === 0">
                <h4 class="title-decoration-1 mb-16">
                  {{ $t('common.otherSetting') }}
                </h4>
                <el-form-item :label="$t('views.knowledge.form.file_count_limit.label')">
                  <el-slider
                    v-model="form.file_count_limit"
                    show-input
                    :show-input-controls="false"
                    :min="1"
                    :max="1000"
                    class="custom-slider"
                  />
                </el-form-item>
                <el-form-item>
                  <template #label>
                    <div class="flex align-center">
                      <span class="mr-4"
                      >{{ $t('views.knowledge.form.file_size_limit.label') }}
                      </span>
                      <el-tooltip
                        effect="dark"
                        :content="$t('views.knowledge.form.file_size_limit.placeholder')"
                        placement="right"
                      >
                        <AppIcon iconName="app-warning" class="app-warning-icon"></AppIcon>
                      </el-tooltip>
                    </div>
                  </template>
                  <el-slider
                    v-model="form.file_size_limit"
                    show-input
                    :show-input-controls="false"
                    :min="1"
                    :max="1000"
                    class="custom-slider"
                  />
                </el-form-item>
              </div>
            </el-form>
            <div class="text-right">
              <el-button
                @click="submit"
                type="primary"
                v-if="!route.path.includes('share/') && permissionPrecise.edit(id)"
              >
                {{ $t('common.save') }}
              </el-button
              >
            </div>
          </div>
        </el-scrollbar>
      </div>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import {ref, onMounted, reactive, computed} from 'vue'
import {useRoute} from 'vue-router'
import BaseForm from '@/views/knowledge/component/BaseForm.vue'
import {MsgSuccess, MsgConfirm} from '@/utils/message'
import {t} from '@/locales'
import {i18n_name} from '@/utils/common'
import permissionMap from '@/permission'
import useStore from '@/stores'

import {loadSharedApi} from '@/utils/dynamics-api/shared-api'

const route = useRoute()
const { user } = useStore()
const {
  params: {id, folderId},
} = route as any

const apiType = computed(() => {
  if (route.path.includes('shared')) {
    return 'systemShare'
  } else if (route.path.includes('resource-management')) {
    return 'systemManage'
  } else {
    return 'workspace'
  }
})

const permissionPrecise = computed(() => {
  return permissionMap['knowledge'][apiType.value]
})

const isShared = computed(() => {
  return folderId === 'share'
})

const webFormRef = ref()
const BaseFormRef = ref()
const loading = ref(false)
const detail = ref<any>({ })
const cloneModelId = ref('')
const user_options = ref<any[]>([])
const selectedCreator = ref('')

const form = ref<any>({
  source_url: '',
  selector: '',
  app_id: '',
  app_secret: '',
  folder_token: '',
  file_count_limit: 50,
  file_size_limit: 100,
})

const rules = reactive({
  source_url: [
    {
      required: true,
      message: t('views.knowledge.form.source_url.requiredMessage'),
      trigger: 'blur',
    },
  ],
  app_id: [
    {
      required: true,
      message: t('views.application.applicationAccess.larkSetting.appIdPlaceholder'),
      trigger: 'blur',
    },
  ],
  app_secret: [
    {
      required: true,
      message: t('views.application.applicationAccess.larkSetting.appSecretPlaceholder'),
      trigger: 'blur',
    },
  ],
  folder_token: [
    {
      required: true,
      message: t('views.application.applicationAccess.larkSetting.folderTokenPlaceholder'),
      trigger: 'blur',
    },
  ],
})

async function submit() {
  if (await BaseFormRef.value?.validate()) {
    await webFormRef.value.validate((valid: any) => {
      if (valid) {
        const obj =
          detail.value.type === 1 || detail.value.type === 2
            ? {
              meta: form.value,
              file_count_limit: form.value.file_count_limit,
              file_size_limit: form.value.file_size_limit,
              create_user: selectedCreator.value,
              user_id: selectedCreator.value,
              ...BaseFormRef.value.form,
            }
            : {
              file_count_limit: form.value.file_count_limit,
              file_size_limit: form.value.file_size_limit,
              create_user: selectedCreator.value,
              user_id: selectedCreator.value,
              ...BaseFormRef.value.form,
            }

        if (cloneModelId.value !== BaseFormRef.value.form.embedding_model_id) {
          MsgConfirm(t('common.tip'), t('views.knowledge.tip.updateModeMessage'), {
            confirmButtonText: t('views.knowledge.setting.vectorization'),
          })
            .then(() => {
              if (detail.value.type === 2) {
                loadSharedApi({type: 'knowledge', systemType: apiType.value})
                  .putLarkKnowledge(id, obj, loading)
                  .then(() => {
                    loadSharedApi({type: 'knowledge', systemType: apiType.value})
                      .putReEmbeddingKnowledge(id)
                      .then(() => {
                        MsgSuccess(t('common.saveSuccess'))
                        // 更新页面上显示的创建者信息
                        const selectedUser = user_options.value.find(user => user.id === selectedCreator.value)
                        if (selectedUser) {
                          detail.value.create_user = selectedUser.id
                          detail.value.user_id = selectedUser.id
                          detail.value.nick_name = selectedUser.nick_name
                        }
                      })
                  })
              } else {
                loadSharedApi({type: 'knowledge', systemType: apiType.value})
                  .putKnowledge(id, obj, loading)
                  .then(() => {
                    loadSharedApi({type: 'knowledge', systemType: apiType.value})
                      .putReEmbeddingKnowledge(id)
                      .then(() => {
                        MsgSuccess(t('common.saveSuccess'))
                        // 更新页面上显示的创建者信息
                        const selectedUser = user_options.value.find(user => user.id === selectedCreator.value)
                        if (selectedUser) {
                          detail.value.create_user = selectedUser.id
                          detail.value.user_id = selectedUser.id
                          detail.value.nick_name = selectedUser.nick_name
                        }
                      })
                  })
              }
            })
            .catch(() => {
            })
        } else {
          if (detail.value.type === 2) {
            loadSharedApi({type: 'knowledge', systemType: apiType.value})
              .putLarkKnowledge(id, obj, loading)
              .then(() => {
                MsgSuccess(t('common.saveSuccess'))
                // 更新页面上显示的创建者信息
                const selectedUser = user_options.value.find(user => user.id === selectedCreator.value)
                if (selectedUser) {
                  detail.value.create_user = selectedUser.id
                  detail.value.nick_name = selectedUser.nick_name
                }
              })
          } else {
            loadSharedApi({type: 'knowledge', systemType: apiType.value})
              .putKnowledge(id, obj, loading)
                  .then(() => {
                    MsgSuccess(t('common.saveSuccess'))
                    // 更新页面上显示的创建者信息
                    const selectedUser = user_options.value.find(user => user.id === selectedCreator.value)
                    if (selectedUser) {
                      detail.value.create_user = selectedUser.id
                      detail.value.nick_name = selectedUser.nick_name
                    }
                  })
          }
        }
      }
    })
  }
}

function getDetail() {
  loadSharedApi({type: 'knowledge', isShared: isShared.value, systemType: apiType.value})
    .getKnowledgeDetail(id, loading)
    .then((res: any) => {
      detail.value = res.data
      cloneModelId.value = res.data?.embedding_model_id
      // 优先使用user_id，如果不存在则使用create_user
      selectedCreator.value = res.data?.user_id || res.data?.create_user || ''
      if (detail.value?.type === 0) {
        form.value.file_count_limit = res.data.file_count_limit
        form.value.file_size_limit = res.data.file_size_limit
      }
      if (detail.value?.type === 1 || detail.value?.type === 2) {
        form.value = res.data.meta
      }
      // 如果有用户列表，尝试找到对应的用户信息来更新nick_name
      if (user_options.value.length > 0 && selectedCreator.value) {
        const selectedUser = user_options.value.find(user => user.id === selectedCreator.value)
        if (selectedUser) {
          detail.value.nick_name = selectedUser.nick_name
        }
      }
    })
}

function getUserList() {
  loadSharedApi({ type: 'workspace', isShared: isShared.value, systemType: apiType.value })
    .getAllMemberList(user.getWorkspaceId(), loading)
    .then((res: any) => {
      user_options.value = res.data
      // 如果已经有selectedCreator的值，尝试找到对应的用户信息来更新nick_name
      if (selectedCreator.value) {
        const selectedUser = user_options.value.find(user => user.id === selectedCreator.value)
        if (selectedUser) {
          detail.value.nick_name = selectedUser.nick_name
        }
      }
    })
}

onMounted(() => {
  getDetail()
  getUserList()
})
</script>
<style lang="scss" scoped>
.knowledge-setting {
  width: 70%;
  margin: 0 auto;
}

.creator-info-descriptions {
  width: 100%;
}

.creator-info-item {
  padding: 8px 12px;
}

.creator-select {
  width: 100%;
  min-width: 180px;
}

.creator-text {
  display: inline-block;
  width: 100%;
  min-width: 180px;
}

/* 调整描述项标签的宽度，确保标签和内容对齐 */
:deep(.el-descriptions__label) {
  padding-right: 8px;
  white-space: nowrap;
}

/* 调整描述项内容的宽度，确保内容有足够的空间 */
:deep(.el-descriptions__content) {
  padding-left: 8px;
  flex: 1;
}
</style>
