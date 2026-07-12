import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { 
  fetchAllCourses, 
  selectCourses, 
  selectCoursesLoading, 
  selectCoursesError 
} from '../features/courses/courseSlice';
import CourseCard from '../components/CourseCard';

const CoursesPage = () => {
  const dispatch = useDispatch();
  const courses = useSelector(selectCourses);
  const loading = useSelector(selectCoursesLoading);
  const error = useSelector(selectCoursesError);
  useEffect(() => {
    dispatch(fetchAllCourses());
  }, [dispatch]);

  return (
    <div className="courses-container">
      <h1>Available Courses</h1>

      {loading && (
        <div className="status-box loading" role="status">
          <p>Loading course catalog...</p>
        </div>
      )}

      {error && (
        <div className="status-box error" role="alert">
          <p><strong>Error:</strong> {error}</p>
          <button onClick={() => dispatch(fetchAllCourses())}>Try Again</button>
        </div>
      )}

      {!loading && !error && (
        <div className="course-grid">
          {courses.map((course) => (
            <CourseCard key={course.id} course={course} />
          ))}
        </div>
      )}
    </div>
  );
};

export default CoursesPage;