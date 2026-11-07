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
  background:
    radial-gradient(ellipse at 18% 0%, rgba(12, 88, 172, 0.26), transparent 44%),
    linear-gradient(110deg, #020916 0%, #06162b 56%, #08172b 100%);
  border-bottom: 1px solid rgba(76, 182, 255, 0.34);
  box-shadow: 0 8px 26px rgba(2, 12, 29, 0.22);
}

.main-nav {
  max-width: 1440px;
  min-height: 98px;
  margin: 0 auto;
  padding: 8px 28px;
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
  width: min(390px, 52vw);
  height: 82px;
  object-fit: contain;
  object-position: left center;
  filter: drop-shadow(0 0 9px rgba(20, 148, 255, 0.22));
  transition: filter 180ms ease, transform 180ms ease;
}

.brand:hover .brand-logo {
  filter: drop-shadow(0 0 13px rgba(33, 176, 255, 0.42));
  transform: translateY(-1px);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav-link {
  text-decoration: none;
  color: #d4e5f8;
  font-weight: 650;
  padding: 10px 15px;
  border: 1px solid transparent;
  border-radius: 9px;
  white-space: nowrap;
  transition: color 160ms ease, background 160ms ease, border-color 160ms ease;
}

.nav-link:hover {
  color: #fff;
  background: rgba(67, 157, 238, 0.12);
  border-color: rgba(96, 182, 255, 0.2);
}

.nav-link.router-link-active {
  color: #eaf8ff;
  background: linear-gradient(135deg, rgba(13, 118, 231, 0.36), rgba(11, 61, 122, 0.36));
  border-color: rgba(89, 190, 255, 0.48);
  box-shadow: inset 0 0 14px rgba(22, 145, 255, 0.12), 0 0 12px rgba(12, 111, 219, 0.12);
}

@media (max-width: 680px) {
  .main-nav {
    min-height: 80px;
    padding: 7px 14px;
    gap: 10px;
  }

  .brand-logo {
    width: min(290px, 51vw);
    height: 64px;
  }

  .nav-links {
    gap: 3px;
  }

  .nav-link {
    padding: 9px 10px;
    font-size: 0.88rem;
  }
}

@media (max-width: 420px) {
  .main-nav {
    padding-inline: 9px;
    gap: 4px;
  }

  .brand-logo {
    width: 44vw;
    height: 54px;
  }

  .nav-links {
    gap: 0;
  }

  .nav-link {
    padding: 8px 7px;
    font-size: 0.8rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    transition-duration: 0.01ms !important;
  }
}
</style>
