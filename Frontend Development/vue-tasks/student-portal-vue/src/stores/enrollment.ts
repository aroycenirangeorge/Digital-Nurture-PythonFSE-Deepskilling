import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { getCourseById } from '../api/courseApi'; // Import your API client

export const useEnrollmentStore = defineStore('enrollment', () => {

  const enrolledCourses = ref<any[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const totalCredits = computed(() => {
    return enrolledCourses.value.reduce((total, course) => total + (course.credits || 0), 0);
  });


  async function fetchAndEnroll(courseId: string | number) {
    try {
      loading.value = true;
      error.value = null;

      const remoteCourse = await getCourseById(courseId);
  
      const exists = enrolledCourses.value.some((c) => c.id === remoteCourse.id);
      if (!exists) {
        enrolledCourses.value.push(remoteCourse);
        console.log(`[Pinia Async Action] Successfully fetched and enrolled in: ${remoteCourse.name}`);
      } else {
        throw new Error(`Already enrolled in course ID ${courseId}`);
      }
    } catch (err: any) {
      error.value = err.message || 'Failed to enroll in course';
      console.error('[Pinia Async Error]:', error.value);
      throw err; 
    } finally {
      loading.value = false;
    }
  }

  function enroll(course: any) {
    if (!enrolledCourses.value.some((c) => c.id === course.id)) {
      enrolledCourses.value.push(course);
    }
  }

  function unenroll(courseId: number | string) {
    enrolledCourses.value = enrolledCourses.value.filter((c) => c.id !== courseId);
  }

  function $reset() {
    enrolledCourses.value = [];
    loading.value = false;
    error.value = null;
    console.log('[Pinia Store] State reset to initial values.');
  }

  return { 
    enrolledCourses, 
    loading, 
    error, 
    totalCredits, 
    fetchAndEnroll, 
    enroll, 
    unenroll, 
    $reset 
  };
});