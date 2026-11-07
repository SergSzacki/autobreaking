<template>
  <div class="app-shell">
    <header class="site-header">
      <nav class="main-nav" aria-label="Main navigation">
        <router-link to="/" class="brand" aria-label="AutoBreaking home">
          <img class="brand-logo" src="/logo.svg" alt="S.Szacki" />
        </router-link>

        <div class="nav-links">
          <router-link to="/" class="nav-link">Cars</router-link>
          <router-link to="/inventory" class="nav-link">Inventory</router-link>
        </div>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: #f3f6fb;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: #ffffff;
  border-bottom: 1px solid #e7edf7;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
}

.main-nav {
  max-width: 1440px;
  min-height: 78px;
  margin: 0 auto;
  padding: 10px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.brand {
  display: inline-flex;
  align-items: center;
  min-width: 0;
  text-decoration: none;
}

.brand-logo {
  display: block;
  width: min(250px, 42vw);
  height: 58px;
  object-fit: contain;
  object-position: left center;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  text-decoration: none;
  color: #1f2937;
  font-weight: 700;
  padding: 9px 13px;
  border-radius: 8px;
  white-space: nowrap;
}

.nav-link:hover {
  background: #f3f6fb;
}

.nav-link.router-link-active {
  background: #eaf1ff;
  color: #1d4ed8;
}

@media (max-width: 520px) {
  .main-nav {
    min-height: 68px;
    padding: 8px 12px;
    gap: 8px;
  }

  .brand-logo {
    width: 150px;
    height: 46px;
  }

  .nav-links {
    gap: 2px;
  }

  .nav-link {
    padding: 8px;
    font-size: 0.85rem;
  }
}
</style>
