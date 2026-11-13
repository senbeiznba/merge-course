import httpx

BASE = "http://localhost:8000"
CASES = [
    ("email already taken", "/students", {"name": "Aigerim Two", "email": "aigerim@example.com"}),
    ("already enrolled", "/enrollments", {"courseId": "ai-integration", "studentId": 3}),
    ("unknown course", "/enrollments", {"courseId": "nope", "studentId": 3}),
    ("unknown student", "/enrollments", {"courseId": "web-security", "studentId": 999}),
    ("name too short", "/students", {"name": "N", "email": "n@example.com"}),
]

for title, path, body in CASES:
    res = httpx.post(BASE + path, json=body)
    print(f"[{res.status_code}] {title} -> Body preview: {res.text[:100]}")