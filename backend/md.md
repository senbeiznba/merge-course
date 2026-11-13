http://localhost:8000/docs
http://localhost:8000/graphql
1
query {
  courses {
    id
    title
  }
  students {
    id
    name
    email
  }
}
2
mutation {
  addStudent(name: "Amir Tak", email: "amir.graphql@example.com") {
    id
    name
    email
  }
}
3
mutation {
  enrollStudent(studentId: 1, courseId: "backend-fastapi") {
    id
    studentId
    courseId
  }
}
query {
  enrollments {
    id
    studentId
    courseId
  }
}