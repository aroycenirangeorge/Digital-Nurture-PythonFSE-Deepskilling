-- TASK 1

INSERT INTO students VALUES (NULL,'Antony', 'George', 'antony.george@college.edu', '2005-12-24', 1, 2023), (NULL,'Royce', 'Niran', 'royce.niran@college.edu', '2005-11-01', 2, 2023);
SELECT * FROM students;
SELECT COUNT(*) FROM students;

UPDATE enrollments SET grade='B' WHERE student_id=5 AND course_id=1;
SELECT student_id, course_id, grade from enrollments;

DELETE FROM enrollments WHERE grade IS NULL;
SELECT * FROM enrollments;

-- TASK 2

SELECT * FROM students WHERE enrollment_year=2022 ORDER BY last_name ASC;

SELECT * FROM courses WHERE credits>3 ORDER BY credits DESC;

SELECT * FROM professors WHERE salary BETWEEN 80000 AND 95000;

SELECT * FROM students WHERE email LIKE "%@college.edu";

SELECT enrollment_year, count(*) FROM students GROUP BY enrollment_year;

-- TASK 3

SELECT CONCAT(s.first_name,' ',s.last_name) AS full_name, d.dept_name FROM students s JOIN departments d ON s.department_id=d.department_id; 

SELECT CONCAT(s.first_name,' ',s.last_name) AS full_name, c.course_name FROM enrollments e JOIN students s ON s.student_id=e.student_id JOIN courses c ON c.course_id=e.course_id;

SELECT CONCAT(s.first_name,' ',s.last_name) AS full_name FROM students s LEFT JOIN enrollments e ON s.student_id=e.student_id WHERE e.enrollment_id IS NULL;

SELECT c.course_name, count(*) FROM courses c LEFT JOIN enrollments e ON c.course_id=e.course_id GROUP BY c.course_name;

SELECT d.dept_name, p.prof_name, p.salary FROM departments d LEFT JOIN professors p ON d.department_id = p.department_id;

-- TASK 4

SELECT c.course_name, count(*) AS enrollment_count FROM courses c JOIN enrollments e ON e.course_id=c.course_id GROUP BY c.course_name;

SELECT d.dept_name, ROUND(AVG(p.salary),2) FROM departments d JOIN professors p GROUP BY d.dept_name;

SELECT * FROM departments WHERE budget>600000;

SELECT e.grade, count(*) FROM students s JOIN enrollments e ON s.student_id=e.student_id JOIN courses c ON c.course_id=e.course_id WHERE c.course_code='CS101' GROUP BY e.grade;

SELECT d.dept_name, COUNT(DISTINCT e.student_id) AS total_students FROM departments d JOIN courses c ON d.department_id = c.department_id JOIN enrollments e ON c.course_id = e.course_id GROUP BY d.department_id, d.dept_name HAVING COUNT(DISTINCT e.student_id) > 2;

