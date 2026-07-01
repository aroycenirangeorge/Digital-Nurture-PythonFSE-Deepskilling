# student_service/app.py
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'student-secret-key'

STUDENTS_DB = {
    101: {"id": 101, "first_name": "AJ Royce Niran", "last_name": "George", "email": "aj@sec.edu"},
}
ENROLLMENTS_DB = []

@app.route('/api/v1/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = STUDENTS_DB.get(student_id)
    if not student:
        return jsonify({"error": "Student not found within this domain"}), 404
    return jsonify(student), 200

@app.route('/api/v1/enrollments/', methods=['POST'])
def create_enrollment():
    data = request.get_json() or {}
    student_id = data.get("student_id")
    course_id = data.get("course_id")
    
    if not student_id or not course_id:
        return jsonify({"error": "Missing student_id or course_id fields"}), 400
        
    if student_id not in STUDENTS_DB:
        return jsonify({"error": "Student does not exist in student database"}), 404

    
    enrollment_record = {"id": len(ENROLLMENTS_DB) + 1, "student_id": student_id, "course_id": course_id}
    ENROLLMENTS_DB.append(enrollment_record)
    return jsonify(enrollment_record), 201

if __name__ == '__main__':
    app.run(port=5002, debug=True)