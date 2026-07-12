<template>
  <header class="app-header">
    <div class="header-top">
      <img src="https://vuejs.org/images/logo.png" alt="Vue Framework Logo" class="logo" />
      <h1>Student Portal</h1>
      
      <div class="badge" role="status" aria-label="Enrolled courses count">
        Enrolled: <strong>{{ store.enrolledCourses.length }}</strong>
      </div>

      <button 
        id="menu-toggle"
        class="menu-btn" 
        :aria-expanded="isMenuOpen.toString()" 
        aria-controls="main-nav"
        aria-label="Toggle navigation menu"
        @click="toggleMenu">
        ☰
      </button>
    </div>

    <nav id="main-nav" aria-label="Main navigation" :hidden="!isMenuOpen && isMobile">
      <router-link 
        to="/" 
        :aria-current="$route.path === '/' ? 'page' : undefined">
        Home
      </router-link>
      <router-link 
        to="/courses" 
        :aria-current="$route.path === '/courses' ? 'page' : undefined">
        Courses
      </router-link>
      <router-link 
        to="/profile" 
        :aria-current="$route.path === '/profile' ? 'page' : undefined">
        Profile
      </router-link>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import { useEnrollmentStore } from '../stores/enrollment';

const store = useEnrollmentStore();
const route = useRoute();
const isMenuOpen = ref(true);
const isMobile = ref(false);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const checkScreenSize = () => {
  isMobile.value = window.innerWidth < 768;
  if (!isMobile.value) isMenuOpen.value = true;
};

onMounted(() => {
  checkScreenSize();
  window.addEventListener('resize', checkScreenSize);
});

onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize);
});
</script>

<style scoped>
.app-header {
  background-color: #42b883;
  color: white;
  padding: 1rem 2rem;
}
.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}
.logo {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}
h1 {
  font-size: 1.5rem;
  margin: 0;
  flex-grow: 1;
}
.badge {
  background: rgba(0, 0, 0, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}
.menu-btn {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
}
nav {
  margin-top: 1rem;
  display: flex;
  gap: 1.5rem;
}
nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}
nav a[aria-current="page"] {
  text-decoration: underline;
  background-color: rgba(0, 0, 0, 0.15);
}

@media (max-width: 768px) {
  .menu-btn { display: block; }
  nav {
    flex-direction: column;
    width: 100%;
    margin-top: 1rem;
  }
}
</style>