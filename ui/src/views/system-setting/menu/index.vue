<template>
  <div class="menu-setting p-16-24">
    <el-breadcrumb separator-icon="ArrowRight" class="mb-16">
      <el-breadcrumb-item>{{ t('views.system.subTitle') }}</el-breadcrumb-item>
      <el-breadcrumb-item>
        <h5 class="ml-4 color-text-primary">{{ $t('views.system.menu.title') }}</h5>
      </el-breadcrumb-item>
    </el-breadcrumb>

    <el-row :gutter="16">
      <el-col :lg="7" :xl="6" :md="9" :sm="24" :xs="24">
        <el-card class="menu-setting__panel" style="--el-card-padding: 16px" v-loading="loading">
          <div class="flex-between mb-12">
            <div>
              <h4 class="mb-4">{{ $t('views.system.menu.userList') }}</h4>
              <div class="color-secondary">{{ $t('views.system.menu.userListTip') }}</div>
            </div>
            <el-tag type="info" effect="plain">{{ filteredUsers.length }}</el-tag>
          </div>

          <el-input
            v-model="keyword"
            clearable
            :placeholder="$t('views.system.menu.searchUserPlaceholder')"
            class="mb-12"
          />

          <div class="menu-setting__user-list">
            <div
              v-for="item in filteredUsers"
              :key="item.id"
              class="menu-setting__user-item"
              :class="{ 'is-active': currentUser?.id === item.id }"
              @click="selectUser(item.id)"
            >
              <div class="flex-between">
                <div>
                  <div class="menu-setting__user-name">{{ item.nick_name }}</div>
                  <div class="menu-setting__user-meta">{{ item.username }}</div>
                </div>
                <el-tag :type="item.is_active ? 'success' : 'info'" effect="light">
                  {{ item.is_active ? $t('common.status.enabled') : $t('common.status.disabled') }}
                </el-tag>
              </div>
              <div class="menu-setting__user-extra">
                <span>{{ item.email || '-' }}</span>
                <span>{{ getCheckedMenuCount(item.id) }} / {{ menuLeafCount }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :lg="17" :xl="18" :md="15" :sm="24" :xs="24">
        <el-card class="menu-setting__panel" style="--el-card-padding: 16px" v-loading="loading">
          <template v-if="currentUser">
            <div class="menu-setting__hero mb-16">
              <div>
                <h4 class="mb-6">{{ currentUser.nick_name }}</h4>
                <div class="color-secondary mb-8">
                  {{ $t('views.system.menu.currentUserTip', { username: currentUser.username }) }}
                </div>
                <div class="menu-setting__hero-tags">
                  <el-tag effect="plain">{{ currentUser.email || currentUser.username }}</el-tag>
                  <el-tag type="success" effect="light">
                    {{ selectedMenuLabels.length }} / {{ menuLeafCount }}
                  </el-tag>
                </div>
              </div>
              <div class="menu-setting__actions">
                <el-button @click="checkAllMenus">{{ $t('views.system.menu.selectAll') }}</el-button>
                <el-button @click="clearAllMenus">{{ $t('views.system.menu.clearAll') }}</el-button>
                <el-button @click="resetCurrentUser">{{ $t('views.system.menu.resetCurrent') }}</el-button>
                <el-button type="primary" :loading="saveLoading" @click="saveCurrentUser">
                  {{ $t('common.save') }}
                </el-button>
              </div>
            </div>

            <div class="menu-setting__summary mb-16">
              <div class="menu-setting__stat-card">
                <div class="menu-setting__stat-label">{{ $t('views.system.menu.selectedCount') }}</div>
                <div class="menu-setting__stat-value">{{ selectedMenuLabels.length }}</div>
              </div>
              <div class="menu-setting__stat-card">
                <div class="menu-setting__stat-label">{{ $t('views.system.menu.hiddenCount') }}</div>
                <div class="menu-setting__stat-value">{{ menuLeafCount - selectedMenuLabels.length }}</div>
              </div>
              <div class="menu-setting__preview-card">
                <div class="menu-setting__block-title mb-10">{{ $t('views.system.menu.previewTitle') }}</div>
                <div class="menu-setting__preview">
                  <template v-if="selectedMenuLabels.length">
                    <el-tag
                      v-for="item in selectedMenuLabels"
                      :key="item"
                      class="mr-8 mb-8"
                      effect="light"
                    >
                      {{ item }}
                    </el-tag>
                  </template>
                  <el-empty v-else :image-size="64" :description="$t('views.system.menu.empty')" />
                </div>
              </div>
            </div>

            <div class="menu-setting__block">
              <div class="flex-between mb-16">
                <div>
                  <div class="menu-setting__block-title">{{ $t('views.system.menu.permissionTitle') }}</div>
                  <div class="color-secondary">{{ $t('views.system.menu.permissionTip') }}</div>
                </div>
              </div>

              <div class="menu-setting__groups">
                <div v-for="group in displayMenuTree" :key="group.id" class="menu-setting__group-card">
                  <div class="flex-between mb-12">
                    <div>
                      <div class="menu-setting__group-title">{{ group.label }}</div>
                      <div class="menu-setting__group-desc">{{ group.description }}</div>
                    </div>
                    <div class="menu-setting__actions">
                      <el-button link type="primary" @click="setGroupMenus(group, true)">
                        {{ $t('views.system.menu.selectAll') }}
                      </el-button>
                      <el-button link type="primary" @click="setGroupMenus(group, false)">
                        {{ $t('views.system.menu.clearAll') }}
                      </el-button>
                    </div>
                  </div>

                  <div class="menu-setting__group-count mb-12">
                    {{ getGroupCheckedCount(group) }} / {{ group.children?.length || 0 }}
                  </div>

                  <div class="menu-setting__menu-grid">
                    <div
                      v-for="menu in group.children"
                      :key="menu.id"
                      class="menu-setting__menu-card"
                      :class="{ 'is-checked': isMenuChecked(menu.id) }"
                      @click="toggleMenu(menu.id)"
                    >
                      <div class="menu-setting__menu-main">
                        <div class="menu-setting__menu-title">{{ menu.label }}</div>
                        <div class="menu-setting__menu-desc">{{ menu.description }}</div>
                      </div>
                      <el-switch
                        :model-value="isMenuChecked(menu.id)"
                        @click.stop
                        @change="setMenuChecked(menu.id, $event)"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { t } from '@/locales'
import { MsgSuccess } from '@/utils/message'
import menuSettingApi from '@/api/system-settings/menu-setting'

type MenuNode = {
  id: string
  label: string
  description?: string
  children?: MenuNode[]
}

type UserItem = {
  id: string
  nick_name: string
  username: string
  email?: string
  is_active: boolean
}

const keyword = ref('')
const loading = ref(false)
const saveLoading = ref(false)
const currentUserId = ref('')
const defaultMenuIds = ['knowledge']
const menuTree = ref<MenuNode[]>([
  {
    id: 'main-navigation-group',
    label: '',
    description: '',
    children: [
      { id: 'application', label: '', description: '' },
      { id: 'mindmap', label: '', description: '' },
      { id: 'knowledge', label: '', description: '' },
      { id: 'tool', label: '', description: '' },
      { id: 'model', label: '', description: '' },
    ],
  },
])
const users = ref<UserItem[]>([])
const checkedMap = ref<Record<string, string[]>>({})

const displayMenuTree = computed(() => localizeMenuTree(menuTree.value))
const menuLeafIds = computed(() => getLeafIds(menuTree.value))
const menuLeafCount = computed(() => menuLeafIds.value.length)
const currentUser = computed(() => users.value.find((item) => item.id === currentUserId.value))

const filteredUsers = computed(() => {
  const text = keyword.value.trim().toLowerCase()
  if (!text) return users.value
  return users.value.filter((item) =>
    [item.nick_name, item.username, item.email || ''].some((value) => value.toLowerCase().includes(text)),
  )
})

const selectedMenuLabels = computed(() => {
  const labelMap = getLeafLabelMap(displayMenuTree.value)
  return (checkedMap.value[currentUserId.value] || []).map((id) => labelMap[id]).filter(Boolean)
})

function localizeMenuTree(list: MenuNode[]): MenuNode[] {
  return list.map((item) => {
    const children = item.children?.length ? localizeMenuTree(item.children) : undefined
    return {
      ...item,
      label: resolveMenuLabel(item.id, item.label),
      description: resolveMenuDescription(item.id, item.description),
      children,
    }
  })
}

function resolveMenuLabel(id: string, fallback = '') {
  const keyMap: Record<string, string> = {
    'main-navigation-group': 'views.system.menu.menuTree.mainNavigation.label',
    application: 'views.system.menu.menuTree.application.label',
    mindmap: 'views.system.menu.menuTree.mindmap.label',
    knowledge: 'views.system.menu.menuTree.knowledge.label',
    tool: 'views.system.menu.menuTree.tool.label',
    model: 'views.system.menu.menuTree.model.label',
  }
  const key = keyMap[id]
  return key ? t(key) : fallback
}

function resolveMenuDescription(id: string, fallback = '') {
  const keyMap: Record<string, string> = {
    'main-navigation-group': 'views.system.menu.menuTree.mainNavigation.description',
    application: 'views.system.menu.menuTree.application.description',
    mindmap: 'views.system.menu.menuTree.mindmap.description',
    knowledge: 'views.system.menu.menuTree.knowledge.description',
    tool: 'views.system.menu.menuTree.tool.description',
    model: 'views.system.menu.menuTree.model.description',
  }
  const key = keyMap[id]
  return key ? t(key) : fallback
}

function getLeafIds(list: MenuNode[]): string[] {
  return list.flatMap((item) => (item.children?.length ? getLeafIds(item.children) : [item.id]))
}

function getLeafLabelMap(list: MenuNode[]) {
  return list.reduce(
    (acc, item) => {
      if (item.children?.length) {
        Object.assign(acc, getLeafLabelMap(item.children))
      } else {
        acc[item.id] = item.label
      }
      return acc
    },
    {} as Record<string, string>,
  )
}

function getCheckedIds(userId = currentUserId.value) {
  return checkedMap.value[userId] || []
}

function getCheckedMenuCount(userId: string) {
  return getCheckedIds(userId).length
}

function normalizeCheckedMap(raw: Record<string, string[]>) {
  const next: Record<string, string[]> = {}
  const leafIds = menuLeafIds.value
  users.value.forEach((item) => {
    const checkedIds = raw[item.id]?.filter((id) => leafIds.includes(id))
    next[item.id] = checkedIds ? [...checkedIds] : defaultMenuIds.filter((id) => leafIds.includes(id))
  })
  return next
}

function isMenuChecked(menuId: string) {
  return getCheckedIds().includes(menuId)
}

function setMenuChecked(menuId: string, checked: string | number | boolean) {
  const checkedIds = new Set(getCheckedIds())
  if (checked) {
    checkedIds.add(menuId)
  } else {
    checkedIds.delete(menuId)
  }
  checkedMap.value[currentUserId.value] = [...checkedIds]
}

function toggleMenu(menuId: string) {
  setMenuChecked(menuId, !isMenuChecked(menuId))
}

function setGroupMenus(group: MenuNode, checked: boolean) {
  const ids = group.children?.map((item) => item.id) || []
  const checkedIds = new Set(getCheckedIds())
  ids.forEach((id) => {
    if (checked) {
      checkedIds.add(id)
    } else {
      checkedIds.delete(id)
    }
  })
  checkedMap.value[currentUserId.value] = [...checkedIds]
}

function getGroupCheckedCount(group: MenuNode) {
  return (group.children || []).filter((item) => isMenuChecked(item.id)).length
}

function selectUser(userId: string) {
  currentUserId.value = userId
}

function checkAllMenus() {
  checkedMap.value[currentUserId.value] = [...menuLeafIds.value]
}

function clearAllMenus() {
  checkedMap.value[currentUserId.value] = []
}

function resetCurrentUser() {
  checkedMap.value[currentUserId.value] = [...defaultMenuIds]
  MsgSuccess(t('views.system.menu.resetSuccess'))
}

async function saveCurrentUser() {
  if (!currentUserId.value) return
  try {
    await menuSettingApi.putMenuSetting(
      {
        user_id: currentUserId.value,
        menu_list: checkedMap.value[currentUserId.value] || [],
      },
      saveLoading,
    )
    MsgSuccess(t('views.system.menu.saveSuccess'))
  } catch (error) {
    return
  }
}

async function loadMenuSetting() {
  try {
    const response = await menuSettingApi.getMenuSetting(loading)
    users.value = response.data?.users || []
    menuTree.value = response.data?.menu_tree?.length ? response.data.menu_tree : menuTree.value
    checkedMap.value = normalizeCheckedMap(response.data?.checked_map || {})
  } catch (error) {
    users.value = []
    checkedMap.value = {}
  }
}

onMounted(async () => {
  await loadMenuSetting()
  currentUserId.value = users.value[0]?.id || ''
})
</script>

<style lang="scss" scoped>
.menu-setting {
  &__panel {
    min-height: calc(100vh - 150px);
  }

  &__hero {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
    padding: 18px 20px;
    border-radius: 14px;
    background: linear-gradient(135deg, #f8fbff 0%, #eef5ff 100%);
    border: 1px solid #dbeafe;
  }

  &__hero-tags,
  &__actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  &__summary {
    display: grid;
    grid-template-columns: 180px 180px minmax(0, 1fr);
    gap: 16px;
    align-items: stretch;
  }

  &__user-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    max-height: calc(100vh - 260px);
    overflow: auto;
    padding-right: 4px;
  }

  &__user-item {
    padding: 14px;
    border: 1px solid var(--el-border-color-light);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    background: #fff;

    &:hover,
    &.is-active {
      border-color: var(--el-color-primary-light-5);
      background: var(--el-color-primary-light-9);
      box-shadow: 0 10px 20px rgba(24, 144, 255, 0.08);
    }
  }

  &__user-name,
  &__group-title,
  &__menu-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }

  &__user-meta,
  &__user-extra,
  &__group-desc,
  &__menu-desc,
  &__group-count {
    font-size: 13px;
    color: var(--el-text-color-secondary);
  }

  &__user-extra {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
  }

  &__block {
    padding: 16px;
    border-radius: 12px;
    background: var(--app-view-bg-color);
    border: 1px solid var(--el-border-color-lighter);
  }

  &__block-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }

  &__preview-card,
  &__stat-card,
  &__group-card,
  &__menu-card {
    background: #fff;
    border: 1px solid var(--el-border-color-light);
    border-radius: 14px;
  }

  &__stat-card {
    padding: 16px;
  }

  &__stat-label {
    font-size: 13px;
    color: var(--el-text-color-secondary);
    margin-bottom: 8px;
  }

  &__stat-value {
    font-size: 30px;
    font-weight: 600;
    color: var(--el-text-color-primary);
    line-height: 1;
  }

  &__preview-card {
    padding: 16px;
    min-height: 112px;
  }

  &__preview {
    min-height: 56px;
  }

  &__groups {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }

  &__group-card {
    padding: 16px;
  }

  &__menu-grid {
    display: grid;
    gap: 12px;
  }

  &__menu-card {
    padding: 14px;
    display: flex;
    justify-content: space-between;
    gap: 12px;
    align-items: center;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover,
    &.is-checked {
      border-color: var(--el-color-primary-light-5);
      box-shadow: 0 12px 24px rgba(24, 144, 255, 0.08);
    }
  }

  &__menu-main {
    min-width: 0;
  }
}

@media (max-width: 1200px) {
  .menu-setting {
    &__summary,
    &__groups {
      grid-template-columns: 1fr;
    }
  }
}
</style>
