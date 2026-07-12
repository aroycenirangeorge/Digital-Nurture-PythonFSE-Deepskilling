import { useParams } from 'react-router-dom';

export default function CourseDetailPage() {
  const { courseId } = useParams();
  return <h1>Details for Course ID: {courseId}</h1>;
}