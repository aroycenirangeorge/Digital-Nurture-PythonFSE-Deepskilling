import { createContext, useState } from 'react';

export const EnrollmentContext = createContext();

export function EnrollmentProvider({ children }) {
  const [enrolledCourses, setEnrolledCourses] = useState([]);

  const enroll = (course) => {
    setEnrolledCourses((prev) => [...prev, course]);
  };

  const unenroll = (courseId) => {
    setEnrolledCourses((prev) => prev.filter(c => c.id !== courseId));
  };

  return (
    <EnrollmentContext.Provider value={{ enrolledCourses, enroll, unenroll }}>
      {children}
    </EnrollmentContext.Provider>
  );
}