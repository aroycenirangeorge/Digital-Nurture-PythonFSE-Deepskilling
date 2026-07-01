# course_service/app.py
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'course-secret-key'

COURSES_DB = {
    1: {"id": 1, "name": "VLSI Hardware Acceleration", "code": "EE302", "credits": 4},
    2: {"id": 2, "name": "Embedded Systems Design", "code": "EE305", "credits": 3}
}

@app.route('/api/v1/courses/', methods=['GET'])
def get_courses():
    return jsonify(list(COURSES_DB.values())), 200

@app.route('/api/v1/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = COURSES_DB.get(course_id)
    if not course:
        return jsonify({"error": "Course not found within this domain"}), 404
    return jsonify(course), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)