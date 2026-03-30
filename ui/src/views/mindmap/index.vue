<template>
  <div class="mindmap-container">
    <div v-if="loading" class="loading">
      加载中...
    </div>
    <div v-else class="mindmap-content">
      <iframe
        :src="mindmapUrl"
        style="width: 100%; height: 100%; border: none;"
        title="思维导图"
      ></iframe>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import systemConfigApi from '@/api/system-settings/system-config'

const mindmapUrl = ref<string>('')
const loading = ref(false)

onMounted(() => {
  loading.value = true
  systemConfigApi.getSystemConfig(loading).then((res: any) => {
    if (res.data && res.data.mindmap_url) {
      mindmapUrl.value = res.data.mindmap_url
    }
  }).catch((err) => {
    console.error('Failed to load mindmap config:', err)
  })
})
</script>

<style scoped>
.mindmap-container {
  height: 100%;
  overflow: hidden;
  position: relative;
}

.mindmap-content {
  height: 100%;
  overflow: hidden;
}

.loading, .error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 16px;
  color: #666;
}

.error {
  color: #f56c6c;
}
</style>
