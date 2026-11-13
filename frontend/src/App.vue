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
    <main><router-view /></main>
    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-mark" aria-hidden="true"><span></span><span></span><span></span></div>
        <p class="copyright">© {{ currentYear }} <strong>S.Szacki</strong> <span class="footer-separator">|</span> Все права защищены</p>
        <p class="rights-notice">
          Материалы сайта, включая тексты, дизайн и программный код, защищены авторским правом.
          Копирование, распространение или использование без предварительного письменного разрешения правообладателя запрещено.
        </p>
        <p class="footer-signature">AUTOBREAKING <span>•</span> DIGITAL GARAGE</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>

<style scoped>
.app-shell { min-height:100vh; display:flex; flex-direction:column; background:#f3f6fb; }
.site-header { position:sticky; top:0; z-index:10; background:radial-gradient(ellipse at 18% 0%,rgba(12,88,172,.26),transparent 44%),linear-gradient(110deg,#020916 0%,#06162b 56%,#08172b 100%); box-shadow:0 8px 22px rgba(2,12,27,.2); }
.main-nav { max-width:1440px; min-height:98px; margin:0 auto; padding:8px 28px; display:flex; align-items:center; justify-content:space-between; gap:24px; }
.brand { display:inline-flex; align-items:center; min-width:0; text-decoration:none; }
.brand-logo { display:block; width:min(390px,52vw); height:82px; object-fit:contain; object-position:left center; filter:drop-shadow(0 0 9px rgba(20,148,255,.22)); transition:filter 180ms ease,transform 180ms ease; }
.brand:hover .brand-logo { filter:drop-shadow(0 0 13px rgba(33,176,255,.42)); transform:translateY(-1px); }
.nav-links { display:flex; align-items:center; gap:10px; }
.nav-link { text-decoration:none; color:#d4e5f8; font-weight:650; padding:10px 15px; border:1px solid transparent; border-radius:9px; white-space:nowrap; transition:color 160ms ease,background 160ms ease,border-color 160ms ease; }
.nav-link:hover { color:#fff; background:rgba(67,157,238,.12); border-color:rgba(96,182,255,.2); }
.nav-link.router-link-active { color:#eaf8ff; background:linear-gradient(135deg,rgba(13,118,231,.36),rgba(11,61,122,.36)); border-color:rgba(89,190,255,.48); box-shadow:inset 0 0 14px rgba(22,145,255,.12); }
main { flex:1; width:100%; }
.site-footer { position:relative; isolation:isolate; overflow:hidden; margin-top:auto; padding:30px 24px 20px; color:#c8d6e8; text-align:center; background:radial-gradient(ellipse at 50% 0%,rgba(0,150,255,.16),transparent 58%),linear-gradient(115deg,#020916 0%,#071a31 48%,#031021 100%); border-top:1px solid rgba(75,190,255,.52); box-shadow:0 -8px 28px rgba(3,18,38,.14); }
.site-footer::before { position:absolute; z-index:-1; inset:0; content:""; opacity:.2; background-image:linear-gradient(rgba(67,170,255,.18) 1px,transparent 1px),linear-gradient(90deg,rgba(67,170,255,.18) 1px,transparent 1px); background-size:28px 28px; mask-image:linear-gradient(to bottom,black,transparent 90%); }
.footer-inner { position:relative; max-width:1000px; margin:0 auto; }
.footer-mark { display:flex; width:68px; height:12px; align-items:center; justify-content:center; gap:5px; margin:0 auto 14px; }
.footer-mark span { display:block; width:6px; height:6px; border:1px solid #45c8ff; border-radius:50%; background:#148ce5; box-shadow:0 0 10px rgba(43,190,255,.8); }
.footer-mark span:nth-child(2) { width:34px; height:2px; border:0; border-radius:2px; background:linear-gradient(90deg,#168eea,#54e3ff); box-shadow:0 0 9px rgba(43,190,255,.65); }
.site-footer p { max-width:1000px; margin:0 auto; line-height:1.55; }
.copyright { color:#e9f7ff; font-weight:650; font-size:.9rem; letter-spacing:.025em; }
.copyright strong { color:#58ccff; text-shadow:0 0 12px rgba(40,166,255,.38); }
.footer-separator { padding:0 7px; color:#3e8fc0; }
.rights-notice { margin-top:7px !important; color:#9fb4ca; font-size:.78rem; }
.footer-signature { margin-top:14px !important; color:#5f7c9a; font-size:.63rem; font-weight:700; letter-spacing:.2em; }
.footer-signature span { padding:0 5px; color:#28b9ff; }
@media(max-width:680px) { .main-nav { min-height:80px; padding:7px 14px; gap:10px; } .brand-logo { width:min(290px,51vw); height:64px; } .nav-links { gap:3px; } .nav-link { padding:9px 10px; font-size:.9rem; } .site-footer { padding:24px 16px 18px; } .rights-notice { font-size:.74rem; } }
@media(max-width:420px) { .main-nav { padding-inline:9px; gap:4px; } .brand-logo { width:44vw; height:54px; } .nav-links { gap:0; } .nav-link { padding:8px 7px; font-size:.8rem; } .footer-separator { padding:0 3px; } }
@media(prefers-reduced-motion:reduce) { *,*::before,*::after { transition-duration:.01ms!important; } }
</style>
