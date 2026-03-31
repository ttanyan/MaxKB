<template>
  <el-dialog
    :title="$t('views.chatLog.feedback.title')"
    v-model="dialogVisible"
    width="600"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <el-form
      ref="formRef"
      :model="form"
      label-position="top"
      require-asterisk-position="right"
      :rules="rules"
      @submit.prevent
    >
      <el-form-item :label="$t('views.chatLog.feedback.type')" prop="feedback_type">
        <el-select v-model="form.feedback_type" :placeholder="$t('views.chatLog.feedback.typePlaceholder')">
          <el-option :label="$t('views.chatLog.feedback.typeSuggestion')" value="SUGGESTION"></el-option>
          <el-option :label="$t('views.chatLog.feedback.typeQuestion')" value="QUESTION"></el-option>
          <el-option :label="$t('views.chatLog.feedback.typeSupplement')" value="SUPPLEMENT"></el-option>
          <el-option :label="$t('views.chatLog.feedback.typeOther')" value="OTHER"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item :label="$t('views.chatLog.feedback.content')" prop="content">
        <el-input
          v-model="form.content"
          type="textarea"
          :placeholder="$t('views.chatLog.feedback.contentPlaceholder')"
          :rows="6"
          maxlength="2000"
          show-word-limit
        ></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click.prevent="dialogVisible = false"> {{ $t('common.cancel') }} </el-button>
        <el-button type="primary" native-type="button" @click.prevent="submitForm(formRef)" :loading="loading">
          {{ $t('common.save') }}
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script setup lang="ts">
import { ref, watch, reactive, computed } from 'vue'
import { useRoute } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { t } from '@/locales'
import { loadSharedApi } from '@/utils/dynamics-api/shared-api'
import chatAPI from '@/api/chat/chat'

const route = useRoute()
const isChatRoute = computed(() => {
  return route.name === 'chat' || typeof route.params?.accessToken === 'string'
})
const apiType = computed(() => {
  if (route.path.includes('resource-management')) {
    return 'systemManage'
  } else {
    return 'workspace'
  }
})

const emit = defineEmits(['refresh'])

const formRef = ref<FormInstance>()
const dialogVisible = ref<boolean>(false)
const loading = ref(false)
const form = ref<any>({
  chat_id: '',
  record_id: '',
  application_id: '',
  feedback_type: '',
  content: '',
})

const rules = reactive<FormRules>({
  feedback_type: [
    { required: true, message: t('views.chatLog.feedback.typeRequired'), trigger: 'blur' },
  ],
  content: [
    { required: true, message: t('views.chatLog.feedback.contentRequired'), trigger: 'blur' },
  ],
})

watch(dialogVisible, (bool) => {
  if (!bool) {
    form.value = {
      chat_id: '',
      record_id: '',
      application_id: '',
      feedback_type: '',
      content: '',
    }
    formRef.value?.clearValidate()
  }
})

const open = (data: any) => {
  form.value.chat_id = data.chat_id
  form.value.record_id = data.record_id || data.id
  form.value.application_id = data.application_id
  formRef.value?.clearValidate()
  dialogVisible.value = true
}

const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      const obj = {
        feedback_type: form.value.feedback_type,
        content: form.value.content,
      }
      const request = isChatRoute.value
        ? chatAPI.postChatRecordFeedback(form.value.chat_id, form.value.record_id, obj, loading)
        : loadSharedApi({ type: 'chatLog', systemType: apiType.value }).postChatRecordFeedback(
            form.value.application_id,
            form.value.chat_id,
            form.value.record_id,
            obj,
            loading,
          )

      request
        .then((res: any) => {
          emit('refresh', res.data)
          dialogVisible.value = false
        })
        .catch(() => undefined)
    }
  })
}

defineExpose({ open })
</script>
<style lang="scss" scoped></style>
