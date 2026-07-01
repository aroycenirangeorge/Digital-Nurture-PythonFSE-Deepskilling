# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Optional

from database import engine, Base, get_db
from models import Course
from schemas import (
    CourseCreate, CoursePatch, CourseResponse, 
    PaginatedCourseResponse, StandardisedErrorResponse
)

app = FastAPI(title="Refactored Best Practices API", version="3.1")

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    code_mapping = {
        404: "NOT_FOUND",
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        422: "VALIDATION_ERROR"
    }
    error_code = code_mapping.get(exc.status_code, "API_ERROR")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": error_code,
                "message": exc.detail,
                "field": getattr(exc, "field", None)
            }
        }
    )


@app.get('/api/v1/courses/', response_model=PaginatedCourseResponse, tags=['Courses'])
async def get_courses_v1(
    request: Request,
    page: int = 1,
    page_size: int = 2,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Page parameters must be greater than zero.")

    query = select(Course)
    count_query = select(func.count()).select_from(Course)

    if search:
        search_filter = f"%{search}%"
        filter_condition = (Course.name.ilike(search_filter)) | (Course.code.ilike(search_filter))
        query = query.filter(filter_condition)
        count_query = count_query.filter(filter_condition)

    total_result = await db.execute(count_query)
    total_count = total_result.scalar() or 0

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    db_result = await db.execute(query)
    courses = db_result.scalars().all()

    base_url = str(request.url).split('?')[0]
    search_param = f"&search={search}" if search else ""
    
    next_url = f"{base_url}?page={page + 1}&page_size={page_size}{search_param}" if (offset + page_size) < total_count else None
    prev_url = f"{base_url}?page={page - 1}&page_size={page_size}{search_param}" if page > 1 else None

    return {
        "count": total_count,
        "next": next_url,
        "previous": prev_url,
        "results": courses
    }


@app.get('/api/v1/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def get_course_v1(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} does not exist")
    return course