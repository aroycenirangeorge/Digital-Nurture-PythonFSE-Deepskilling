<template>
  <div class="profile-container">
    <header class="profile-header">
      <h1>Student Dashboard</h1>
      <button type="button" class="reset-btn" @click="handleReset">
        Reset Enrollment State
      </button>
    </header>

    <section aria-labelledby="summary-heading">
      <h2 id="summary-heading">Academic Summary</h2>
      <div class="summary-box">
        <p>Total Enrolled Courses: <strong>{{ enrolledCourses.length }}</strong></p>
        <p>Total Credits: <strong>{{ totalCredits }}</strong></p>
      </div>
    </section>

    <section aria-labelledby="courses-heading">
      <h2 id="courses-heading">Your Enrolled Courses</h2>
      
      <div v-if="enrolledCourses.length === 0" class="empty-state">
        <p>No active enrollments found. Try enrolling from the Courses page!</p>
      </div>

      <ul v-else class="enrolled-list">
        <li v-for="course in enrolledCourses" :key="course.id" class="enrolled-item">
          <div>
            <h3>{{ course.name }}</h3>
            <p>Code: {{ course.code }} | Credits: {{ course.credits }}</p>
          </div>
          <button 
            type="button" 
            class="remove-btn" 
            @click="unenroll(course.id)">
            Drop Course
          </button>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { useEnrollmentStore } from '../stores/enrollment';

const store = useEnrollmentStore();

// Step 149: Extract state & getters with storeToRefs to maintain reactivity!
const { enrolledCourses, totalCredits } = storeToRefs(store);

// Extract actions directly without storeToRefs
const { unenroll, $reset } = store;

const handleReset = () => {
  if (confirm('Are you sure you want to drop all courses?')) {
    $reset();
  }
};
</script>

<style scoped>
.profile-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.reset-btn { background-color: #64748b; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; }
.reset-btn:hover { background-color: #475569; }
.summary-box { background: #f0fdf4; border: 1px solid #bbf7d0; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; }
.enrolled-list { list-style: none; padding: 0; }
.enrolled-item { display: flex; justify-content: space-between; align-items: center; padding: 1rem; border: 1px solid #ddd; margin-bottom: 0.5rem; border-radius: 6px; }
.remove-btn { background-color: #ff4d4f; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; }
</style>