<template>
  <div class="courses-container">
    <input 
      v-model="searchTerm" 
      type="text" 
      placeholder="Search courses by name..." 
    />
    
    <div v-for="course in filteredCourses" :key="course.id" class="course-item">
      <CourseCard 
        :name="course.name"
        :code="course.code"
        :credits="course.credits"
        :grade="course.grade"
      />
      <button @click="store.enroll(course)" class="enroll-btn">
        Enroll in Course
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import CourseCard from '../components/CourseCard.vue';
import { useEnrollmentStore } from '../stores/enrollment';
import { getAllCourses } from '../api/courseApi'; // Import centralized API

const store = useEnrollmentStore();
const searchTerm = ref('');
const courses = ref([]);
const isLoading = ref(true);
const errorMessage = ref('');

onMounted(async () => {
  try {
    isLoading.value = true;
    errorMessage.value = '';
    // Call the service layer — returns unwrapped data directly!
    courses.value = await getAllCourses();
  } catch (error) {
    errorMessage.value = `Failed to load courses: ${error.message} (Status: ${error.statusCode || 'N/A'})`;
  } finally {
    isLoading.value = false;
  }
});

const filteredCourses = computed(() => {
  return courses.value.filter(course => 
    course.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});
</script>

<style scoped>
.courses-container { padding: 2rem; max-width: 800px; margin: 0 auto; }
input { padding: 0.5rem; width: 100%; margin-bottom: 1rem; }
.course-item { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #eee; padding-bottom: 1rem; }
.enroll-btn { background-color: #42b883; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; font-weight: bold; }
.enroll-btn:hover { background-color: #33a06f; }
</style>