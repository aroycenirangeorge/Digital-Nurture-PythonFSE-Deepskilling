# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from database import engine, Base, get_db
from models import Course
from schemas import CourseCreate, CourseResponse

app = FastAPI(title="Course Management API", version="1.0")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post('/api/courses/', response_model=CourseResponse, status_code=201)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.code == course.code))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Course code already exists")

    db_course = Course(**course.model_dump())
    db.add(db_course)
    await db.commit()  
    await db.refresh(db_course)
    return db_course


@app.get('/api/courses/', response_model=List[CourseResponse])
async def get_courses(
    skip: int = 0, 
    limit: int = 10, 
    department_id: Optional[int] = None, 
    db: AsyncSession = Depends(get_db)
):
    
    query = select(Course)
    
    if department_id is not None:
        query = query.filter(Course.department_id == department_id)
        
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)  # Step 66: await db.execute()
    return result.scalars().all()


@app.get('/api/courses/{course_id}', response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with ID {course_id} not found")
    return course