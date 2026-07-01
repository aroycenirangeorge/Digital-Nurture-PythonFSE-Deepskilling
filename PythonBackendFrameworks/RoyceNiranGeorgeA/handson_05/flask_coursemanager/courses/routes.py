from flask import Blueprint, request, jsonify
from extensions import db
from courses.models import Course, Student, Enrollment, Department

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

def make_response_json(data, status_code):
    envelope = {
        'status': 'success' if status_code in [200, 201] else 'error',
        'data': data
    }
    return jsonify(envelope), status_code


@courses_bp.route('/', methods=['GET'])
def get_courses():
    all_courses = Course.query.all()
    serialized_courses = [course.to_dict() for course in all_courses]
    return make_response_json(serialized_courses, 200)


@courses_bp.route('/', methods=['POST'])
def create_course():
    data = request.get_json()
    
    if data is None:
        return make_response_json({"message": "Invalid or missing JSON payload"}, 400)
        
    required_fields = ['name', 'code', 'credits', 'department_id']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        error_msg = f"Missing required fields: {', '.join(missing_fields)}"
        return make_response_json({"message": error_msg}, 400)
        
    dept_exists = Department.query.get(data['department_id'])
    if not dept_exists:
        return make_response_json({"message": f"Department ID {data['department_id']} does not exist"}, 400)

    existing_code = Course.query.filter_by(code=data['code']).first()
    if existing_code:
        return make_response_json({"message": f"Course code {data['code']} already exists"}, 400)

    new_course = Course(
        name=data['name'],
        code=data['code'],
        credits=data['credits'],
        department_id=data['department_id']
    )
    
    db.session.add(new_course)
    db.session.commit()
    
    return make_response_json(new_course.to_dict(), 201)


@courses_bp.route('/<int:course_id>', methods=['GET', 'PUT', 'DELETE'])
def course_detail(course_id):
    course = Course.query.get_or_404(description=f"Course with ID {course_id} not found")
        
    if request.method == 'GET':
        return make_response_json(course.to_dict(), 200)
        
    elif request.method == 'PUT':
        data = request.get_json() or {}
        
        if 'code' in data and data['code'] != course.code:
            existing_code = Course.query.filter_by(code=data['code']).first()
            if existing_code:
                return make_response_json({"message": f"Course code {data['code']} already exists"}, 400)
        
        course.name = data.get('name', course.name)
        course.code = data.get('code', course.code)
        course.credits = data.get('credits', course.credits)
        course.department_id = data.get('department_id', course.department_id)
        
        db.session.commit()
        return make_response_json(course.to_dict(), 200)
        
    elif request.method == 'DELETE':
        db.session.delete(course)
        db.session.commit()
        return make_response_json({"message": "Course deleted successfully from database"}, 200)


@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def get_course_students(course_id):
    Course.query.get_or_404(course_id)
    
    students_in_course = Student.query.join(Enrollment).filter(Enrollment.course_id == course_id).all()
    
    serialized_students = [student.to_dict() for student in students_in_course]
    return make_response_json(serialized_students, 200)