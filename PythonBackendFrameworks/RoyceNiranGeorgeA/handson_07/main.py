# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Response, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from database import engine, Base, get_db
from models import Course, Student, Enrollment
from schemas import (
    CourseCreate, CourseUpdate, CourseResponse, 
    StudentResponse, EnrollmentCreate, EnrollmentResponse
)

app = FastAPI(
    title="Advanced Course Management System",
    description="An API with fully featured async database configurations, automated Pydantic validations, and background tasks.",
    version="2.0",
    contact={
        "name": "Backend Engineering Support",
        "email": "support@coursemanager.local",
    }
)

def send_confirmation_email(student_email: str):
    print(f"Sending confirmation to {student_email}")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post(
    '/api/enrollments/', 
    response_model=EnrollmentResponse, 
    status_code=status.HTTP_201_CREATED,
    tags=['Enrollments'],
    summary="Enroll a student in a course",
    response_description="The established enrollment confirmation object record."
)
async def create_enrollment(
    enrollment: EnrollmentCreate, 
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    student_check = await db.execute(select(Student).filter(Student.id == enrollment.student_id))
    student = student_check.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    course_check = await db.execute(select(Course).filter(Course.id == enrollment.course_id))
    if not course_check.scalars().first():
        raise HTTPException(status_code=404, detail="Course not found")

    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)

    background_tasks.add_task(send_confirmation_email, student.email)

    return db_enrollment

@app.post('/api/courses/', response_model=CourseResponse, status_code=status.HTTP_201_CREATED, tags=['Courses'])
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.code == course.code))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Course code already exists")
    db_course = Course(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course


@app.get('/api/courses/', response_model=List[CourseResponse], tags=['Courses'])
async def get_courses(skip: int = 0, limit: int = 10, department_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(Course).offset(skip).limit(limit)
    if department_id is not None:
        query = query.filter(Course.department_id == department_id)
    result = await db.execute(query)
    return result.scalars().all()


@app.get('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


@app.put('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def update_course(course_id: int, course_data: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    db_course = result.scalars().first()
    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
    update_dict = course_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_course, key, value)
        
    await db.commit()
    await db.refresh(db_course)
    return db_course


@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    db_course = result.scalars().first()
    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    await db.delete(db_course)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get('/api/courses/{course_id}/students/', response_model=List[StudentResponse], tags=['Courses'])
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    course_check = await db.execute(select(Course).filter(Course.id == course_id))
    if not course_check.scalars().first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    query = select(Student).join(Enrollment, Student.id == Enrollment.student_id).filter(Enrollment.course_id == course_id)
    result = await db.execute(query)
    return result.scalars().all()