import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.config.errorHandler = (err: any, instance, info) => {
  console.error('====================================');
  console.error('[Global Vue Error Handler Triggered]');
  console.error('Error Message:', err?.message || err);
  console.error('Vue Component Info:', info);
  console.error('====================================');

  alert(`An unexpected error occurred: ${err?.message || 'Unknown application error'}. Please refresh the page.`);
};

app.mount('#app');