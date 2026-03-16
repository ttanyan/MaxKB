<template>
  <div
    class="sidebar"
    style="display: flex; flex-direction: column; height: 100%; background-color: #f9fafb; width: 240px;"
  >
    <div style="padding: 16px;"></div>

    <div style="padding: 0 16px;">
      <div v-if="!isSystemManagement" style="display: flex; flex-direction: column; gap: 8px;">
        <router-link
          v-if="user.is_admin() || menuSetting.hasMenu('application')"
          to="/application"
          style="display: block; padding: 10px 16px; border-radius: 8px; text-decoration: none; color: #333; font-size: 14px;"
          :style="activeMainMenu === '/application' ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
        >
          {{ menuText.aiApplication }}
        </router-link>
        <router-link
          v-if="user.is_admin() || menuSetting.hasMenu('mindmap')"
          to="/mindmap"
          style="display: block; padding: 10px 16px; border-radius: 8px; text-decoration: none; color: #333; font-size: 14px;"
          :style="activeMainMenu === '/mindmap' ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
        >
          {{ menuText.mindmap }}
        </router-link>
        <router-link
          v-if="user.is_admin() || menuSetting.hasMenu('knowledge')"
          to="/knowledge"
          style="display: block; padding: 10px 16px; border-radius: 8px; text-decoration: none; color: #333; font-size: 14px;"
          :style="activeMainMenu === '/knowledge' ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
        >
          {{ menuText.knowledge }}
        </router-link>
        <router-link
          v-if="user.is_admin() || menuSetting.hasMenu('tool')"
          to="/tool"
          style="display: block; padding: 10px 16px; border-radius: 8px; text-decoration: none; color: #333; font-size: 14px;"
          :style="activeMainMenu === '/tool' ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
        >
          {{ menuText.toolManagement }}
        </router-link>
        <router-link
          v-if="user.is_admin() || menuSetting.hasMenu('model')"
          to="/model"
          style="display: block; padding: 10px 16px; border-radius: 8px; text-decoration: none; color: #333; font-size: 14px;"
          :style="activeMainMenu === '/model' ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
        >
          {{ menuText.modelManagement }}
        </router-link>
      </div>

      <div v-else style="display: flex; flex-direction: column; gap: 8px;">
        <router-link
          to="/system/user"
          style="display: block; padding: 10px 16px; border-radius: 8px; text-decoration: none; color: #333; font-size: 14px;"
          :style="activeSystemMenu === '/system/user' ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
        >
          {{ menuText.userManagement }}
        </router-link>

        <div>
          <div
            style="display: flex; justify-content: space-between; align-items: center; padding: 10px 16px; border-radius: 8px; cursor: pointer;"
            :style="activeSystemMenu.startsWith('/system/authorization') ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
            @click="toggleResourceAuth"
          >
            <span>{{ menuText.resourceAuthorization }}</span>
            <span>{{ resourceAuthExpanded ? '▾' : '▸' }}</span>
          </div>
          <div
            v-if="resourceAuthExpanded"
            style="padding-left: 32px; margin-top: 4px; display: flex; flex-direction: column; gap: 4px;"
          >
            <router-link
              to="/system/authorization/application"
              style="display: block; padding: 8px 16px; border-radius: 8px; text-decoration: none; color: #666; font-size: 13px;"
              :style="activeSystemMenu === '/system/authorization/application' ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
            >
              {{ menuText.aiApplication }}
            </router-link>
            <router-link
              to="/system/authorization/knowledge"
              style="display: block; padding: 8px 16px; border-radius: 8px; text-decoration: none; color: #666; font-size: 13px;"
              :style="activeSystemMenu === '/system/authorization/knowledge' ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
            >
              {{ menuText.knowledge }}
            </router-link>
            <router-link
              to="/system/authorization/tool"
              style="display: block; padding: 8px 16px; border-radius: 8px; text-decoration: none; color: #666; font-size: 13px;"
              :style="activeSystemMenu === '/system/authorization/tool' ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
            >
              {{ menuText.toolManagement }}
            </router-link>
            <router-link
              to="/system/authorization/model"
              style="display: block; padding: 8px 16px; border-radius: 8px; text-decoration: none; color: #666; font-size: 13px;"
              :style="activeSystemMenu === '/system/authorization/model' ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
            >
              {{ menuText.modelManagement }}
            </router-link>
          </div>
        </div>

        <div>
          <div
            style="display: flex; justify-content: space-between; align-items: center; padding: 10px 16px; border-radius: 8px; cursor: pointer;"
            :style="activeSystemMenu.startsWith('/system/email') ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
            @click="toggleSystemSettings"
          >
            <span>{{ menuText.systemSettings }}</span>
            <span>{{ systemSettingsExpanded ? '▾' : '▸' }}</span>
          </div>
          <div
            v-if="systemSettingsExpanded"
            style="padding-left: 32px; margin-top: 4px; display: flex; flex-direction: column; gap: 4px;"
          >
            <router-link
              to="/system/email"
              style="display: block; padding: 8px 16px; border-radius: 8px; text-decoration: none; color: #666; font-size: 13px;"
              :style="activeSystemMenu === '/system/email' ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
            >
              {{ menuText.emailSettings }}
            </router-link>
            <router-link
              to="/system/setting/menu"
              style="display: block; padding: 8px 16px; border-radius: 8px; text-decoration: none; color: #666; font-size: 13px;"
              :style="activeSystemMenu === '/system/setting/menu' ? { backgroundColor: '#e6f0ff', color: '#1890ff' } : {}"
            >
              {{ menuText.menuManagement }}
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <div style="margin-top: auto; padding: 16px; border-top: 1px solid #e5e7eb;">
      <UserAvatar />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import UserAvatar from '@/layout/layout-header/avatar/index.vue'
import useStore from '@/stores'

const route = useRoute()
const { locale } = useI18n({ useScope: 'global' })
const { user, menuSetting } = useStore()

const menuText = computed(() => {
  if (locale.value === 'en-US') {
    return {
      aiApplication: 'AI Applications',
      mindmap: 'Mind Map',
      knowledge: 'Knowledge Base',
      toolManagement: 'Tool Management',
      modelManagement: 'Model Management',
      userManagement: 'User Management',
      resourceAuthorization: 'Resource Authorization',
      systemSettings: 'System Settings',
      emailSettings: 'Email Settings',
      menuManagement: 'Menu Management',
    }
  }
  if (locale.value === 'zh-Hant') {
    return {
      aiApplication: 'AI應用',
      mindmap: '思維導圖',
      knowledge: '知識庫',
      toolManagement: '工具管理',
      modelManagement: '模型管理',
      userManagement: '用戶管理',
      resourceAuthorization: '資源授權',
      systemSettings: '系統設定',
      emailSettings: '郵件設定',
      menuManagement: '菜單管理',
    }
  }
  return {
    aiApplication: 'AI应用',
    mindmap: '思维导图',
    knowledge: '知识库',
    toolManagement: '工具管理',
    modelManagement: '模型管理',
    userManagement: '用户管理',
    resourceAuthorization: '资源授权',
    systemSettings: '系统设置',
    emailSettings: '邮件设置',
    menuManagement: '菜单管理',
  }
})

const isSystemManagement = computed(() => {
  const path = route.path
  return path.startsWith('/system') || path.startsWith('/admin/system')
})

const activeMainMenu = computed(() => {
  const path = route.path
  if (path.startsWith('/application')) return '/application'
  if (path.startsWith('/mindmap')) return '/mindmap'
  if (path.startsWith('/knowledge')) return '/knowledge'
  if (path.startsWith('/tool')) return '/tool'
  if (path.startsWith('/model')) return '/model'
  return '/application'
})

const activeSystemMenu = computed(() => {
  const path = route.path
  if (path.startsWith('/system/user') || path.startsWith('/admin/system/user')) return '/system/user'
  if (path.startsWith('/system/authorization') || path.startsWith('/admin/system/authorization')) {
    return path.replace('/admin', '')
  }
  if (path.startsWith('/system/email') || path.startsWith('/admin/system/email')) {
    return path.replace('/admin', '')
  }
  if (path.startsWith('/system/setting/menu') || path.startsWith('/admin/system/setting/menu')) {
    return path.replace('/admin', '')
  }
  return '/system/user'
})

const resourceAuthExpanded = ref(false)
const systemSettingsExpanded = ref(false)

const toggleResourceAuth = () => {
  resourceAuthExpanded.value = !resourceAuthExpanded.value
  systemSettingsExpanded.value = false
}

const toggleSystemSettings = () => {
  systemSettingsExpanded.value = !systemSettingsExpanded.value
  resourceAuthExpanded.value = false
}

onMounted(() => {
  resourceAuthExpanded.value = false
  systemSettingsExpanded.value = false
})
</script>
