import apiClient from './apiClient';

export interface Course {
  id: number | string;
  name: string;
  code: string;
  credits: number;
  grade?: string;
}

export const getAllCourses = async (): Promise<Course[]> => {
  const rawData: any[] = await apiClient.get('/users');
  return rawData.slice(0, 5).map((item, index) => ({
    id: item.id,
    name: ['Web Development', 'Python Backend', 'Data Structures', 'Computer Networks', 'AI Infrastructure'][index] || item.name,
    code: ['CS101', 'PY202', 'DSA303', 'NW404', 'AI505'][index] || `GEN${item.id}`,
    credits: [4, 3, 4, 3, 4][index] || 3,
    grade: ['A', 'B', 'A', 'B', 'A'][index] || 'A'
  }));
};

export const getCourseById = async (id: string | number): Promise<Course> => {
  const item: any = await apiClient.get(`/users/${id}`);
  
  return {
    id: item.id,
    name: `${item.name}'s Specialized Course`,
    code: `SPEC${item.id}00`,
    credits: 4
  };
};

export const enrollStudent = async (studentId: string | number, courseId: string | number): Promise<{ success: boolean; message: string }> => {
  const response: any = await apiClient.post('/posts', {
    title: `Enrollment: Student ${studentId}`,
    body: `Enrolled in course ID ${courseId}`,
    userId: studentId
  });

  return {
    success: true,
    message: `Student ${studentId} successfully enrolled in Course ${courseId} (Transaction ID: ${response.id})`
  };
};