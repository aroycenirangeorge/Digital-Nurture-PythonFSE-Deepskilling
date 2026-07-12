<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useEnrollmentStore } from '../stores/enrollment';
import { getCourseById, enrollStudent } from '../api/courseApi';

const route = useRoute();
const router = useRouter();
const store = useEnrollmentStore();

const courseId = computed(() => route.params.id);
const course = ref(null);
const isLoading = ref(true);

onMounted(async () => {
  try {
    isLoading.value = true;
    course.value = await getCourseById(courseId.value);
  } catch (error) {
    console.error('Error fetching course:', error.message);
  } finally {
    isLoading.value = false;
  }
});

const enroll = async () => {
  try {
    // 1. Call API layer to enroll
    const result = await enrollStudent('STU-8842', course.value.id);
    console.log(result.message);
    
    // 2. Update local Pinia state
    store.enroll(course.value);
    
    // 3. Navigate
    router.push('/profile');
  } catch (error) {
    alert(`Enrollment failed: ${error.message}`);
  }
};
</script>