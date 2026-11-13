"""SQLAlchemy database models."""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from db import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    is_elective = Column(Boolean, default=False, nullable=False)

    enrollments = relationship("Enrollment", back_populates="course")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    enrollments = relationship("Enrollment", back_populates="student")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    course = relationship("Course", back_populates="enrollments")
    student = relationship("Student", back_populates="enrollments")