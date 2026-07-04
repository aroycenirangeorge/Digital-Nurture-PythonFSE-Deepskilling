-- TASK 1

CREATE DATABASE college_db;
USE college_db;

CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE,
    department_id INT,
    enrollment_year INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE professors (
    professor_id INT AUTO_INCREMENT PRIMARY KEY,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

INSERT INTO departments (dept_name, hod_name, budget) VALUES
('Computer Science', 'Dr. Ramesh Kumar', 850000.00),
('Electronics', 'Dr. Priya Nair', 620000.00),
('Mechanical', 'Dr. Suresh Iyer', 540000.00),
('Civil', 'Dr. Ananya Sharma', 430000.00);

INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
('Arjun', 'Mehta', 'arjun.mehta@college.edu', '2003-04-12', 1, 2022),
('Priya', 'Suresh', 'priya.suresh@college.edu', '2003-07-25', 1, 2022),
('Rohan', 'Verma', 'rohan.verma@college.edu', '2002-11-08', 2, 2021),
('Sneha', 'Patel', 'sneha.patel@college.edu', '2004-01-30', 3, 2023),
('Vikram', 'Das', 'vikram.das@college.edu', '2003-09-14', 1, 2022),
('Kavya', 'Menon', 'kavyamenon@college.edu', '2002-05-17', 2, 2021),
('Aditya', 'Singh', 'aditya.singh@college.edu', '2004-03-22', 4, 2023),
('Deepika', 'Rao', 'deepika.rao@college.edu', '2003-08-09', 1, 2022);

INSERT INTO courses (course_name, course_code, credits, department_id) VALUES
('Data Structures & Algorithms', 'CS101', 4, 1),
('Database Management Systems', 'CS102', 3, 1),
('Object Oriented Programming', 'CS103', 4, 1),
('Circuit Theory', 'EC101', 3, 2),
('Thermodynamics', 'ME101', 3, 3);

INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
(1, 1, '2022-07-01', 'A'), 
(1, 2, '2022-07-01', 'B'),
(2, 1, '2022-07-01', 'B'), 
(2, 3, '2022-07-01', 'A'),
(3, 4, '2022-07-01', 'A'), 
(4, 5, '2023-07-01', NULL),
(5, 1, '2022-07-01', 'C'), 
(5, 2, '2022-07-01', 'A'),
(6, 4, '2021-07-01', 'B'), 
(7, 5, '2023-07-01', NULL),
(8, 1, '2022-07-01', 'A'), 
(8, 3, '2022-07-01', 'B');

INSERT INTO professors (prof_name, email, department_id, salary) VALUES
('Dr. Anand Krishnan', 'anand.k@college.edu', 1, 95000.00),
('Dr. Meena Pillai', 'meena.p@college.edu', 1, 88000.00),
('Dr. Sunil Rajan', 'sunil.r@college.edu', 2, 82000.00),
('Dr. Latha Gopal', 'latha.g@college.edu', 3, 79000.00),
('Dr. Kartik Bose', 'kartik.b@college.edu', 4, 76000.00);

SHOW TABLES;
DESCRIBE courses;
DESCRIBE departments;
DESCRIBE enrollments;
DESCRIBE professors;
DESCRIBE students;

--TASK 2

-- 1NF Verification:
-- The schema satisfies First Normal Form (1NF) because all tables contain 
-- only atomic (indivisible) values, and there are no repeating groups or 
-- multi-valued attributes. A hypothetical violation would occur if a student 
-- had multiple phone numbers or emails concatenated into a single text column, 
-- which is avoided here by keeping data fields strictly scalar.

-- 2NF Verification:
-- The schema satisfies Second Normal Form (2NF) because it is in 1NF and 
-- all non-key attributes are fully functionally dependent on the primary keys.
-- Looking closely at the 'enrollments' table, the primary key is 'enrollment_id'. 
-- Even if we consider the composite candidate key (student_id, course_id), 
-- the non-key columns 'enrollment_date' and 'grade' depend strictly on the 
-- unique combination of BOTH a specific student taking a specific course. 
-- There are no partial dependencies where a column depends on only part of a key.

-- 3NF Verification & Hint Analysis:
-- The schema satisfies Third Normal Form (3NF) because it is in 2NF and 
-- contains zero transitive dependencies. Non-prime columns depend strictly 
-- on the primary key, and nothing else. 
-- Addressing the hint: Storing 'dept_name' inside the 'students' table 
-- would explicitly violate 3NF. This is because 'dept_name' depends on 
-- 'department_id', which in turn depends on the student's primary key 'student_id' 
-- (student_id -> department_id -> dept_name). This would form a transitive 
-- dependency, causing data redundancy. By keeping 'dept_name' isolated inside the 
-- 'departments' table, the design remains completely normalized and clean.


--TASK 3

ALTER  TABLE students ADD phone_number VARCHAR(15);
DESCRIBE students;

ALTER TABLE courses ADD max_seats INT DEFAULT 60;
DESCRIBE courses;

ALTER TABLE enrollments ADD CONSTRAINT check_grade CHECK (grade IN ('A', 'B', 'C', 'D', 'F'));

ALTER TABLE departments RENAME COLUMN hod_name TO head_of_dept;
DESCRIBE departments;

ALTER TABLE students DROP COLUMN phone_number;
DESCRIBE students;