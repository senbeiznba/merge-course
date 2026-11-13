# Course Catalog API
FastAPI backend for the course catalog (Labs 4–5).

## How to run
```
    python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev main.py
```
Docs: http://localhost:8000/docs

## What changed in Lab 5

### CORS
`CORSMiddleware` allows the origins from the `CORS_ORIGINS` environment variable (comma-separated), default
`http://localhost:3000` (scheme + host + port, no path, no trailing slash). It is needed because the browser
(Client Components: filter, like, enrollment form) calls this API from another origin; without
`access-control-allow-origin` the browser hides the response from JavaScript. Requests from Next.js Server
Components are server-to-server and do not need CORS.
Methods are an explicit list `["GET", "POST"]` and headers `["Content-Type"]`: an explicit list is safer because
a new method or header is not allowed by accident (a preflight with `DELETE` or `Authorization` gets 400
`Disallowed CORS method` / `Disallowed CORS headers`).

```
CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000" fastapi dev main.py   # PowerShell: $env:CORS_ORIGINS="..."
```

### camelCase in JSON
All models inherit `CamelModel` (`alias_generator=to_camel`, `validate_by_name=True`, `validate_by_alias=True`).
Python keeps `is_elective`, JSON uses `isElective`. Query parameters are NOT renamed (`?is_elective=true`).
`validate_by_name=True` is required because `data.py` builds courses by field name.

### New routes
| Route | Result |
| --- | --- |
| `POST /courses/{course_id}/like` | 200, updated course; 404 `{"detail": "Course not found"}` |
| `POST /enrollments` | 201 `{"courseId": "web-security", "studentName": "Aigerim", "id": 1}`; 422 if name < 2 chars; 404 if course is unknown |
| `GET /enrollments` | 200, list of enrollments |

Example like response:
```json
{"id": "web-security", "title": "Web Security Essentials", "description": "...", "credits": 4, "isElective": false, "likes": 22}
```
Example 422 (`loc` uses the JSON name `studentName`):
```json
{"detail": [{"type": "string_too_short", "loc": ["body", "studentName"], "msg": "String should have at least 2 characters"}]}
```
Likes and enrollments live in memory and reset on every restart.
