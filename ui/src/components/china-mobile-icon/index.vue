<template>
  <div class="china-mobile-icon" aria-label="China Mobile">
    <img src="/aiot-header-logo.png" alt="China Mobile" />
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: 'ChinaMobileIcon' })
</script>

<style scoped>
.china-mobile-icon {
  width: var(--china-mobile-icon-width, 176px);
  height: var(--china-mobile-icon-height, 22px);
  /* margin-right: var(--china-mobile-icon-gap, 14px); */
  flex-shrink: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.china-mobile-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}
</style>
