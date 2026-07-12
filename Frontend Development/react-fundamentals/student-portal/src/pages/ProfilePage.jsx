import { useSelector, useDispatch } from 'react-redux';
import { unenroll } from '../redux/enrollmentSlice';

export default function ProfilePage() {
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses);
  const dispatch = useDispatch();

  return (
    <div>
      <h1>My Profile</h1>
      {enrolledCourses.map(c => (
        <div key={c.id}>
          {c.name} <button onClick={() => dispatch(unenroll(c.id))}>Remove</button>
        </div>
      ))}
    </div>
  );
}