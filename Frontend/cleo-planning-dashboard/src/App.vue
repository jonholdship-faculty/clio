<template>
  <div class="app-container">
    <header class="app-header">
      <div class="container">
        <div class="header-content">
          <div class="logo-container">
            <div class="logo">CLIO</div>
            <div class="subtitle">Planning Office Records System</div>
          </div>
          <nav class="top-nav">
            <router-link to="/" class="nav-link">Home</router-link>
            <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
            <div class="user-profile">
              <span class="user-avatar">CS</span>
            </div>
          </nav>
        </div>
      </div>
    </header>
    <main class="app-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <footer class="app-footer">
      <div class="container">
        <div class="footer-content">
          <div>© 2025 Clio Planning System</div>
          <div class="footer-links">
            <a href="#" class="footer-link">Terms</a>
            <a href="#" class="footer-link">Privacy</a>
            <a href="#" class="footer-link">Contact</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const currentTheme = ref('default');

const setTheme = (theme) => {
  const bodyElement = document.body;
  const htmlElement = document.documentElement;
  
  // Remove all theme classes 
  bodyElement.classList.remove('govuk-theme');
  
  // Store the selected theme in localStorage
  localStorage.setItem('clio-theme', theme);
  
  // Handle GOV.UK theme separately
  if (theme === 'govuk') {
    bodyElement.classList.add('govuk-theme');
    // Ensure GOV.UK specific classes are present
    htmlElement.classList.add('govuk-template');
    bodyElement.classList.add('govuk-template__body', 'js-enabled', 'govuk-frontend-supported');
  } else {
    // Remove GOV.UK specific classes if they're present
    htmlElement.classList.remove('govuk-template');
    bodyElement.classList.remove('govuk-template__body', 'js-enabled', 'govuk-frontend-supported');
  }
  
  currentTheme.value = theme;
};

// Check if there's a stored theme on initial load
onMounted(() => {
  const storedTheme = localStorage.getItem('clio-theme');
  if (storedTheme) {
    currentTheme.value = storedTheme;
    setTheme(storedTheme);
  }
});
</script>

<style>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background-color: var(--primary);
  color: white;
  padding: var(--spacing-md) 0;
  box-shadow: var(--shadow-md);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-container {
  display: flex;
  flex-direction: column;
}

.logo {
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.subtitle {
  font-size: 0.75rem;
  opacity: 0.9;
}

.top-nav {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  opacity: 0.8;
  transition: opacity var(--transition-normal);
}

.nav-link:hover, .nav-link.router-link-active {
  opacity: 1;
}

.user-profile {
  margin-left: var(--spacing-md);
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  background-color: var(--accent);
  color: white;
  border-radius: 50%;
  font-weight: 600;
  cursor: pointer;
  transition: transform var(--transition-normal);
}

.user-avatar:hover {
  transform: scale(1.05);
}

.app-content {
  flex: 1;
  background-color: var(--background);
  padding: var(--spacing-xl) 0;
}

.app-footer {
  background-color: white;
  padding: var(--spacing-md) 0;
  color: var(--text-light);
  border-top: 1px solid var(--border);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-links {
  display: flex;
  gap: var(--spacing-md);
}

.footer-link {
  color: var(--text-light);
  text-decoration: none;
  transition: color var(--transition-normal);
}

.footer-link:hover {
  color: var(--primary);
}

/* Theme styles */
body.dark {
  --primary: #3b82f6;
  --primary-light: #60a5fa;
  --primary-dark: #2563eb;
  --secondary: #94a3b8;
  --accent: #a855f7;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --info: #06b6d4;
  --background: #0f172a;
  --card: #1e293b;
  --text: #f1f5f9;
  --text-light: #94a3b8;
  --border: #334155;
  --shadow: rgba(0, 0, 0, 0.25);
}

body.vibrant {
  --primary: #8b5cf6;
  --primary-light: #a78bfa;
  --primary-dark: #7c3aed;
  --secondary: #6366f1;
  --accent: #ec4899;
  --success: #06b6d4;
  --warning: #f97316;
  --danger: #ef4444;
  --info: #3b82f6;
  --background: #f8fafc;
  --card: #ffffff;
  --text: #334155;
  --text-light: #64748b;
  --border: #e2e8f0;
  --shadow: rgba(0, 0, 0, 0.04);
}

body.govuk-theme {
  /* GOV.UK color palette */
  --primary: #005ea5; /* GOV.UK blue */
  --primary-light: #1d70b8;
  --primary-dark: #003078;
  --secondary: #505a5f;
  --accent: #ffdd00; /* Yellow */
  --success: #00703c; /* Green */
  --warning: #f47738; /* Orange */
  --danger: #d4351c; /* Red */
  --info: #1d70b8; /* Light blue */
  --background: #f3f2f1; /* Light grey background */
  --card: #ffffff;
  --text: #0b0c0c; /* Black text */
  --text-light: #505a5f;
  --border: #b1b4b6;
  --shadow: rgba(0, 0, 0, 0.1);

  /* GDS Transport font */
  font-family: "GDS Transport", arial, sans-serif;
  
  /* GOV.UK specific spacing */
  --govuk-gutter: 30px;
  --govuk-gutter-half: 15px;
  --spacing-md: 20px;
  --spacing-lg: 30px;
  --spacing-xl: 40px;
  --spacing-2xl: 60px;
}

/* Additional GOV.UK specific styles for the app header when GOV.UK theme is active */
body.govuk-theme .app-header {
  background-color: #0b0c0c; /* Black header */
  color: white;
  padding: 15px 0;
  border-bottom: 10px solid #1d70b8;
}

body.govuk-theme .logo-container {
  margin-right: 15px;
}

body.govuk-theme .top-nav {
  margin-top: 10px;
}

body.govuk-theme .app-content {
  padding-top: 60px;
  padding-bottom: 60px;
}

body.govuk-theme .app-footer {
  border-top: none;
  background-color: #0b0c0c;
  color: white;
  padding: 45px 0 30px;
}

body.govuk-theme .footer-link {
  color: white;
}

body.govuk-theme .btn {
  font-family: "GDS Transport", arial, sans-serif;
  font-weight: 400;
  font-size: 16px;
  line-height: 1.1875;
  box-sizing: border-box;
  display: inline-block;
  position: relative;
  margin-top: 0;
  margin-bottom: 22px;
  padding: 8px 10px 7px;
  border: 2px solid transparent;
  border-radius: 0;
  color: #ffffff;
  background-color: #00703c;
  box-shadow: 0 2px 0 #002d18;
  text-align: center;
  vertical-align: top;
  cursor: pointer;
  -webkit-appearance: none;
  text-decoration: none;
}

body.govuk-theme .btn:hover {
  background-color: #005a30;
}

body.govuk-theme .nav-link.router-link-active {
  text-decoration: underline;
  font-weight: 700;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .top-nav {
    width: 100%;
    justify-content: center;
    overflow-x: auto;
    padding-bottom: var(--spacing-sm);
  }
  
  .footer-content {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }
}
</style>
