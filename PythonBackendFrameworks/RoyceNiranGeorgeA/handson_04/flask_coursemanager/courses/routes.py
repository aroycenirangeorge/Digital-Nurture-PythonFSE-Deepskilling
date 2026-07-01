from flask import Blueprint, request, jsonify

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# Simulated in-memory database storage for tracking courses
mock_courses_db = [
    {"id": 1, "name": "Computer Science Introduction", "code": "CS101", "credits": 4},
    {"id": 2, "name": "Basic Circuit Analysis", "code": "EE101", "credits": 3}
]

def make_response_json(data, status_code):
    """Step 44: Helper function ensuring a consistent JSON envelope layout."""
    envelope = {
        'status': 'success' if status_code in [200, 201] else 'error',
        'data': data
    }
    return jsonify(envelope), status_code

@courses_bp.route('/', methods=['GET'])
def get_courses():
    return make_response_json(mock_courses_db, 200)

@courses_bp.route('/', methods=['POST'])
def create_course():
    """Step 42: Parse data payload and enforce strict field validations."""
    data = request.get_json()
    
    # Catch empty payloads or missing Content-Type headers gracefully
    if data is None:
        return make_response_json({"message": "Invalid or missing JSON payload"}, 400)
        
    required_fields = ['name', 'code', 'credits']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        error_msg = f"Missing required fields: {', '.join(missing_fields)}"
        return make_response_json({"message": error_msg}, 400)
        
    new_course = {
        "id": max([c['id'] for c in mock_courses_db], default=0) + 1,
        "name": data['name'],
        "code": data['code'],
        "credits": data['credits']
    }
    mock_courses_db.append(new_course)
    return make_response_json(new_course, 201)

@courses_bp.route('/<int:course_id>', methods=['GET', 'PUT', 'DELETE'])
def course_detail(course_id):
    """Step 43: Handle item-specific GET, PUT, and DELETE operations."""
    # Move the global declaration to the very top of the function
    global mock_courses_db
    
    course = next((c for c in mock_courses_db if c['id'] == course_id), None)
    
    if not course:
        return make_response_json({"message": f"Course with ID {course_id} not found"}, 404)
        
    if request.method == 'GET':
        return make_response_json(course, 200)
        
    elif request.method == 'PUT':
        data = request.get_json() or {}
        course.update({
            "name": data.get('name', course['name']),
            "code": data.get('code', course['code']),
            "credits": data.get('credits', course['credits'])
        })
        return make_response_json(course, 200)
        
    elif request.method == 'DELETE':
        # Remove the global keyword from here since it's now at the top
        mock_courses_db = [c for c in mock_courses_db if c['id'] != course_id]
        return make_response_json({"message": "Course deleted successfully"}, 200)