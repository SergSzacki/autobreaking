<template>
  <div class="app-shell">
    <nav class="main-nav">
      <router-link to="/" class="nav-link">Cars</router-link>
      <router-link to="/inventory" class="nav-link">Inventory</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: #f3f6fb;
}

.main-nav {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 16px 24px;
  background: #ffffff;
  border-bottom: 1px solid #e7edf7;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.03);
}

.nav-link {
  text-decoration: none;
  color: #1f2937;
  font-weight: 700;
  padding: 8px 12px;
  border-radius: 8px;
}

.nav-link.router-link-active {
  background: #eaf1ff;
  color: #1d4ed8;
}
</style>
