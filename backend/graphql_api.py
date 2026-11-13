"""GraphQL API using Strawberry."""

import strawberry
from sqlalchemy.orm import Session
from db import SessionLocal
from models import (
    Course as CourseModel,
    Student as StudentModel,
    Enrollment as EnrollmentModel,
)

@strawberry.type
class Course:
    id: str
    title: str
    description: str
    credits: int
    likes: int
    is_elective: bool

    @classmethod
    def from_model(cls, m: CourseModel) -> "Course":
        return cls(
            id=m.id,
            title=m.title,
            description=m.description,
            credits=m.credits,
            likes=m.likes,
            is_elective=m.is_elective,
        )

@strawberry.type
class Student:
    id: int
    name: str
    email: str

    @classmethod
    def from_model(cls, m: StudentModel) -> "Student":
        return cls(
            id=m.id,
            name=m.name,
            email=m.email,
        )

@strawberry.type
class Enrollment:
    id: int
    student_id: int
    course_id: str

    @classmethod
    def from_model(cls, m: EnrollmentModel) -> "Enrollment":
        return cls(
            id=m.id,
            student_id=m.student_id,
            course_id=m.course_id,
        )

@strawberry.type
class Query:
    @strawberry.field
    def courses(self, is_elective: bool | None = None, sort: str = "popular") -> list[Course]:
        db: Session = SessionLocal()
        try:
            from sqlalchemy import select
            stmt = select(CourseModel)
            if is_elective is not None:
                stmt = stmt.where(CourseModel.is_elective == is_elective)
            
            if sort == "title":
                stmt = stmt.order_by(CourseModel.title)
            else:
                stmt = stmt.order_by(CourseModel.likes.desc(), CourseModel.id)
                
            models = db.scalars(stmt).all()
            return [Course.from_model(m) for m in models]
        finally:
            db.close()

    @strawberry.field
    def students(self) -> list[Student]:
        db: Session = SessionLocal()
        try:
            from sqlalchemy import select
            stmt = select(StudentModel)
            models = db.scalars(stmt).all()
            return [Student.from_model(m) for m in models]
        finally:
            db.close()

    @strawberry.field
    def enrollments(self) -> list[Enrollment]:
        db: Session = SessionLocal()
        try:
            from sqlalchemy import select
            stmt = select(EnrollmentModel)
            models = db.scalars(stmt).all()
            return [Enrollment.from_model(m) for m in models]
        finally:
            db.close()

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_student(self, name: str, email: str) -> Student:
        db: Session = SessionLocal()
        try:
            db_student = StudentModel(name=name, email=email)
            db.add(db_student)
            db.commit()
            db.refresh(db_student)
            return Student.from_model(db_student)
        finally:
            db.close()

    @strawberry.mutation
    def add_course(
        self, id: str, title: str, description: str, credits: int, is_elective: bool = False
    ) -> Course:
        db: Session = SessionLocal()
        try:
            db_course = CourseModel(
                id=id,
                title=title,
                description=description,
                credits=credits,
                likes=0,
                is_elective=is_elective
            )
            db.add(db_course)
            db.commit()
            db.refresh(db_course)
            return Course.from_model(db_course)
        finally:
            db.close()

    @strawberry.mutation
    def enroll_student(self, student_id: int, course_id: str) -> Enrollment:
        db: Session = SessionLocal()
        try:
            db_enrollment = EnrollmentModel(student_id=student_id, course_id=course_id)
            db.add(db_enrollment)
            db.commit()
            db.refresh(db_enrollment)
            return Enrollment.from_model(db_enrollment)
        finally:
            db.close()

schema = strawberry.Schema(query=Query, mutation=Mutation)