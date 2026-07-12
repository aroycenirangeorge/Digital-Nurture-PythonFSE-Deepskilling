import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';

export default function Header() {
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses);
  return (
    <nav style={{ padding: '10px', borderBottom: '1px solid #ccc' }}>
      <Link to="/">Home</Link> | <Link to="/courses">Courses</Link> | <Link to="/profile">Profile</Link>
      <span> Enrolled: {enrolledCourses.length}</span>
    </nav>
  );
}