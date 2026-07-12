<template>
  <div class="card">
    <h3>{{ name }}</h3>
    <p><strong>Code:</strong> {{ code }}</p>
    <p><strong>Credits:</strong> {{ credits }}</p>
    <p><strong>Grade:</strong> {{ grade }}</p>
  </div>
</template>

<script setup>
defineProps({
  name: String,
  code: String,
  credits: Number,
  grade: String
});
</script>

<style scoped>
.card {
  border: 1px solid #ddd;
  padding: 1rem;
  margin: 10px 0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>