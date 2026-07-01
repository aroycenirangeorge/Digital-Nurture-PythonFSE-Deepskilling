# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt

from database import get_db
from models import User, Course
from schemas import TokenResponse, CourseCreate, CourseResponse
from security import oauth2_scheme, verify_password, create_access_token, SECRET_KEY, ALGORITHM

app = FastAPI(title="Secure Production API", version="4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Step 94: Allow local frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_410_GONE or status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user


@app.post('/api/v1/auth/login', response_model=TokenResponse, tags=['Authentication'])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post('/api/v1/courses/', response_model=CourseResponse, status_code=201, tags=['Courses'])
async def create_course(
    course: CourseCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Enforces route protection
):
    result = await db.execute(select(Course).filter(Course.code == course.code))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Course code already exists")
        
    db_course = Course(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course