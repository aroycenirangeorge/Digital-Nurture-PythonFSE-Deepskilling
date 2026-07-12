import { useDispatch } from 'react-redux';
import { enroll } from '../redux/enrollmentSlice';
import { useNavigate } from 'react-router-dom';

export default function CourseCard({ id, name, code }) {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  return (
    <div style={{ border: '1px solid #ddd', padding: '10px', margin: '10px' }}>
      <h3>{name}</h3>
      <button onClick={() => { dispatch(enroll({ id, name, code })); navigate('/profile'); }}>
        Enroll
      </button>
    </div>
  );
}