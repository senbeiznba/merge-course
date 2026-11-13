from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Course, Enrollment, Student

CONSTRAINT_ERRORS = {
    "students_email_key": ("EMAIL_TAKEN", "Student with this email already exists"),
    "enrollments_course_id_student_id_key": ("ALREADY_ENROLLED", "Student is already enrolled in this course"),
    "enrollments_course_id_fkey": ("COURSE_NOT_FOUND", "Course not found"),
    "enrollments_student_id_fkey": ("STUDENT_NOT_FOUND", "Student not found"),
}


class ServiceError(Exception):
    """Expected error: carries a code that REST and GraphQL translate differently."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def commit(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        constraint_name = getattr(exc.orig.diag, "constraint_name", None)
        if constraint_name in CONSTRAINT_ERRORS:
            code, message = CONSTRAINT_ERRORS[constraint_name]
            raise ServiceError(code, message) from exc
        raise


def create_student(db: Session, name: str, email: str) -> Student:
    # Бонусное правило для проверки имени
    if len(name.strip()) < 2:
        raise ServiceError("INVALID_NAME", "Name must have at least 2 characters")
        
    student = Student(name=name, email=email)
    db.add(student)
    commit(db)
    db.refresh(student)
    return student


def enroll(db: Session, course_id: str, student_id: int) -> Enrollment:
    # Проверяем существование курса и студента перед добавлением, 
    # чтобы поймать внешние ключи или выдать корректную ошибку через ServiceError
    course = db.get(Course, course_id)
    if not course:
        raise ServiceError("COURSE_NOT_FOUND", "Course not found")

    student = db.get(Student, student_id)
    if not student:
        raise ServiceError("STUDENT_NOT_FOUND", "Student not found")

    enrollment = Enrollment(course_id=course_id, student_id=student_id)
    db.add(enrollment)
    commit(db)
    db.refresh(enrollment)
    return enrollment


def like_course(db: Session, course_id: str) -> Course:
    stmt = (
        update(Course)
        .where(Course.id == course_id)
        .values(likes=Course.likes + 1)
        .returning(Course)
    )
    course = db.scalars(stmt).one_or_none()
    if course is None:
        raise ServiceError("COURSE_NOT_FOUND", "Course not found")
    commit(db)
    db.refresh(course)
    return course