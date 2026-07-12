-- TASK 1

SELECT 
    s.student_id, 
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    COUNT(*) AS enrollment_count
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(*) > (
    SELECT AVG(course_count) 
    FROM (
        SELECT COUNT(*) AS course_count 
        FROM enrollments 
        GROUP BY student_id
    ) AS student_counts
);

SELECT c.course_id, c.course_code, c.course_name
FROM courses c
WHERE EXISTS (SELECT 1 FROM enrollments e WHERE e.course_id = c.course_id) -- Ensures the course has at least one student
  AND NOT EXISTS (
      SELECT 1 
      FROM enrollments e 
      WHERE e.course_id = c.course_id 
        AND (e.grade != 'A' OR e.grade IS NULL)
  );

SELECT p1.prof_name, p1.department_id, p1.salary
FROM professors p1
WHERE p1.salary = (
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p1.department_id
);

SELECT dept_avgs.dept_name, dept_avgs.average_salary
FROM (
    SELECT 
        d.dept_name, 
        AVG(p.salary) AS average_salary
    FROM departments d
    JOIN professors p ON d.department_id = p.department_id
    GROUP BY d.department_id, d.dept_name
) AS dept_avgs
WHERE dept_avgs.average_salary > 85000;


-- TASK 2

CREATE OR REPLACE VIEW vw_student_enrollment_summary AS
SELECT 
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name AS department,
    COUNT(e.course_id) AS courses_enrolled,
    ROUND(AVG(CASE 
        WHEN e.grade = 'A' THEN 4
        WHEN e.grade = 'B' THEN 3
        WHEN e.grade = 'C' THEN 2
        WHEN e.grade = 'D' THEN 1
        WHEN e.grade = 'F' THEN 0
        ELSE NULL 
    END), 2) AS gpa
FROM students s
LEFT JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

CREATE OR REPLACE VIEW vw_course_stats AS
SELECT 
    c.course_name,
    c.course_code,
    COUNT(e.student_id) AS total_enrollments,
    ROUND(AVG(CASE 
        WHEN e.grade = 'A' THEN 4
        WHEN e.grade = 'B' THEN 3
        WHEN e.grade = 'C' THEN 2
        WHEN e.grade = 'D' THEN 1
        WHEN e.grade = 'F' THEN 0
        ELSE NULL 
    END), 2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

SELECT * 
FROM vw_student_enrollment_summary 
WHERE gpa > 3.00;

UPDATE vw_student_enrollment_summary 
SET department = 'Computer Science' 
WHERE full_name = 'Antony George';

DROP VIEW IF EXISTS vw_course_stats;
DROP VIEW IF EXISTS vw_student_enrollment_summary;

CREATE VIEW vw_student_enrollment_summary AS
SELECT student_id, first_name, last_name, email, department_id, enrollment_year
FROM students
WHERE department_id = 1
WITH CHECK OPTION;


-- TASK 3

DELIMITER $$

CREATE PROCEDURE sp_enroll_student(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_enrollment_date DATE
)
BEGIN
    DECLARE v_exists INT DEFAULT 0;

    SELECT COUNT(*) INTO v_exists 
    FROM enrollments 
    WHERE student_id = p_student_id AND course_id = p_course_id;

    IF v_exists > 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Duplicate Enrollment Error: This student is already enrolled in this course.';
    ELSE
        INSERT INTO enrollments (student_id, course_id, enrollment_date) 
        VALUES (p_student_id, p_course_id, p_enrollment_date);
    END IF;
END $$

DELIMITER ;

CREATE TABLE IF NOT EXISTS department_transfer_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    old_department_id INT,
    new_department_id INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id INT,
    IN p_new_dept_id INT
)
BEGIN
    DECLARE v_old_dept_id INT;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    SELECT department_id INTO v_old_dept_id 
    FROM students 
    WHERE student_id = p_student_id;

    START TRANSACTION;
        UPDATE students 
        SET department_id = p_new_dept_id 
        WHERE student_id = p_student_id;

        INSERT INTO department_transfer_log (student_id, old_department_id, new_department_id)
        VALUES (p_student_id, v_old_dept_id, p_new_dept_id);
    COMMIT;
END $$

DELIMITER ;

SELECT student_id, department_id FROM students WHERE student_id = 1;

CALL sp_transfer_student(1, 9999);

SELECT student_id, department_id FROM students WHERE student_id = 1;
SELECT * FROM department_transfer_log WHERE student_id = 1;

START TRANSACTION;

    INSERT INTO enrollments (student_id, course_id, enrollment_date) 
    VALUES (1, 2, '2026-07-12');

    SAVEPOINT first_insert_saved;

    INSERT INTO enrollments (student_id, course_id, enrollment_date) 
    VALUES (9999, 3, '2026-07-12');

    ROLLBACK TO SAVEPOINT first_insert_saved;

COMMIT;

SELECT * FROM enrollments WHERE enrollment_date = '2026-07-12';

