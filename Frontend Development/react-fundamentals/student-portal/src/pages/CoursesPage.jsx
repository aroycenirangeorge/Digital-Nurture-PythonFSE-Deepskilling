import CourseCard from '../components/CourseCard';

export default function CoursesPage() {
  const courses = [
    { id: 1, name: 'Web Dev', code: 'CS101' },
    { id: 2, name: 'Python', code: 'CS102' }
  ];
  return (
    <div>
      <h1>Courses</h1>
      {courses.map(c => <CourseCard key={c.id} {...c} />)}
    </div>
  );
} 
