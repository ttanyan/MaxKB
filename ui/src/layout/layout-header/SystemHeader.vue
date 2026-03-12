<template>
  <div class="app-top-bar-container border-b flex-center">
    <div class="header-content flex-between w-full align-center">
      <div class="header-left">
        <ChinaMobileIcon class="header-icon" />
        <!-- <h1 class="header-title">{{ isSystemManagement ? 'AI-RAG | 系统管理' : 'AI-RAG' }}</h1> -->
        <h1 class="header-title">AI-RAG</h1>
      </div>
      <div class="header-right">
        <router-link v-if="isSystemManagement" to="/application" class="back-link">
          <span class="back-icon">&larr;</span>
          返回工作空间
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import ChinaMobileIcon from '@/components/china-mobile-icon/index.vue'

const route = useRoute()

const isSystemManagement = computed(() => {
  const path = route.path
  return path.startsWith('/system') || path.startsWith('/admin/system')
})
</script>

<style lang="scss" scoped>
.app-top-bar-container {
  height: var(--app-header-height);
  box-sizing: border-box;
  // padding: var(--app-header-padding);
  padding-right: 20px;
}

.header-content {
  // padding: 0 16px;
}

.header-left {
  display: flex;
  align-items: center;
}

:deep(.header-icon) {
  --china-mobile-icon-width: 192px;
  --china-mobile-icon-height: 24px;
  --china-mobile-icon-gap: 16px;
}

.header-title {
  margin: 0;
  font-size: 18px;
  line-height: 1;
  font-weight: 700;
  letter-spacing: 0.3px;
  background: linear-gradient(90deg, #6b47e5, #1e71c7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.header-right {
  display: flex;
  align-items: center;
}

.back-link {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 6px;
  text-decoration: none;
  color: #1890ff;
  border: 1px solid #1890ff;
}

.back-icon {
  margin-right: 4px;
}
</style>
