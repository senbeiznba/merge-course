import os
import problem
import services
import models

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter
from graphql_api import schema

from db import get_db, Base, engine
from models import Course, Enrollment, Student
from schemas import (
    Course as CourseOut,
    CourseCreate,
    Enrollment as EnrollmentOut,
    StudentOut,
    EnrollmentIn,
    StudentIn,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Course Catalog API")
problem.install(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Подключаем GraphQL роутер
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Зависимость для получения сессии базы данных в эндпоинтах
SessionDep = Depends(get_db)


def pagination(page: int = 1, page_size: int = 20):
    return {"offset": (page - 1) * page_size, "limit": page_size}


@app.get("/")
def read_root():
    return {"message": "Course Catalog API is running"}


@app.get("/courses", response_model=list[CourseOut])
def list_courses(
    is_elective: bool | None = None,
    sort: str = "popular",
    p: dict = Depends(pagination),
    db: Session = SessionDep,
):
    from sqlalchemy import select
    stmt = select(Course)
    if is_elective is not None:
        stmt = stmt.where(Course.is_elective == is_elective)
    
    if sort == "title":
        stmt = stmt.order_by(Course.title)
    else:
        stmt = stmt.order_by(Course.likes.desc(), Course.id)
        
    courses = db.scalars(stmt.offset(p["offset"]).limit(p["limit"])).all()
    return courses


@app.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: str, db: Session = SessionDep):
    course = db.get(Course, course_id)
    if course is None:
        raise services.ServiceError("COURSE_NOT_FOUND", "Course not found")
    return course


@app.post("/courses", response_model=CourseOut, status_code=201)
def create_course(course: CourseCreate, db: Session = SessionDep):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.post("/courses/{course_id}/like", response_model=CourseOut)
def like_course(course_id: str, db: Session = SessionDep):
    return services.like_course(db, course_id)


@app.post("/students", response_model=StudentOut, status_code=201)
def create_student(data: StudentIn, db: Session = SessionDep):
    return services.create_student(db, data.name, data.email)


@app.post("/enrollments", response_model=EnrollmentOut, status_code=201)
def create_enrollment(data: EnrollmentIn, db: Session = SessionDep):
    return services.enroll(db, data.course_id, data.student_id)


@app.get("/enrollments", response_model=list[EnrollmentOut])
def list_enrollments(db: Session = SessionDep):
    from sqlalchemy import select
    stmt = select(Enrollment).order_by(Enrollment.id)
    return db.scalars(stmt).all()