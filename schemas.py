from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # aliases in camelCase
        validate_by_name=True,     # also accept the field name
        validate_by_alias=True,    # and the alias
    )


class Course(CamelModel):
    id: str
    title: str
    description: str
    credits: int
    is_elective: bool = False  # in JSON this is isElective
    likes: int = 0


class EnrollmentIn(CamelModel):
    course_id: str
    student_name: str = Field(min_length=2)


class Enrollment(EnrollmentIn):
    id: int
