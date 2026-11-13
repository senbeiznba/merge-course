from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from services import ServiceError

BASE = "https://example.com/problems/"


PROBLEMS = {
    "email-taken": (409, "email-taken", "Email Already Taken"),
    "already-enrolled": (409, "already-enrolled", "Already Enrolled"),
    "course-not-found": (404, "course-not-found", "Course Not Found"),
    "student-not-found": (404, "student-not-found", "Student Not Found"),
    "conflict": (400, "conflict", "Conflict Error"),
}


def problem(
    request: Request,
    status: int,
    title: str,
    detail: str | None = None,
    type: str = "about:blank",
    headers: dict | None = None,
    **extra,
) -> JSONResponse:
    body = {
        "type": type,
        "title": title,
        "status": status,
    }
    if detail is not None:
        body["detail"] = detail
    body["instance"] = request.url.path
    body.update(extra)

    return JSONResponse(
        body,
        status_code=status,
        headers=headers,
        media_type="application/problem+json",
    )


def install(app: FastAPI) -> None:
    @app.exception_handler(ServiceError)
    async def on_service_error(request: Request, exc: ServiceError):
        status, end_type, title = PROBLEMS[exc.code]
        return problem(
            request,
            status=status,
            title=title,
            detail=exc.message,
            type=BASE + end_type,
        )
    @app.exception_handler(RequestValidationError)
    async def on_validation_error(request: Request, exc: RequestValidationError):
        errors = [
            {
                "in": err["loc"][0],
                "field": ".".join(str(part) for part in err["loc"][1:]),
                "detail": err["msg"],
            }
            for err in exc.errors()
        ]
        text = f"{len(errors)} invalid value(s) in the request"
        return problem(
            request,
            422,
            "Validation failed",
            text,
            type=BASE + "validation-error",
            errors=errors,
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def on_http_error(request: Request, exc: StarletteHTTPException):
        status = exc.status_code
        title = HTTPStatus(status).phrase
        detail = exc.detail if exc.detail != title else None
        return problem(
            request,
            status=status,
            title=title,
            detail=detail,
            headers=exc.headers,
        )