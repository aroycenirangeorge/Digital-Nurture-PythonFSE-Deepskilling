from pydantic import BaseModel
from typing import List, Optional


class CourseBase(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int

class CourseCreate(CourseBase):
    pass

class CoursePatch(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True


class DepartmentBase(BaseModel):
    name: str
    head_of_dept: Optional[str] = None
    budget: Optional[float] = None

class DepartmentResponse(DepartmentBase):
    id: int
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True
    
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentResponse(EnrollmentCreate):
    id: int

    class Config:
        from_attributes = True

from typing import Any, Optional, List

class PaginatedCourseResponse(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[CourseResponse]

class ErrorDetail(BaseModel):
    code: str
    message: str
    field: Optional[str] = None

class StandardisedErrorResponse(BaseModel):
    error: ErrorDetail