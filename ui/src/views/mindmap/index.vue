<template>
  <div class="mindmap-container">
    <div class="mindmap-content">
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
}

.mindmap-content {
  height: 100%;
  overflow: hidden;
}
</style>
