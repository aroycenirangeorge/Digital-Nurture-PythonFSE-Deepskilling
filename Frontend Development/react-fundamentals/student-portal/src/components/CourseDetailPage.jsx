import { useParams } from 'react-router-dom';

export default function CourseDetailPage() {
  const { courseId } = useParams();
  return <h2>Viewing Details for Course: {courseId}</h2>;
}