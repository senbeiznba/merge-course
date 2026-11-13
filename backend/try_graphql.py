import httpx

BASE = "http://localhost:8000/graphql"

# GraphQL запрос для получения курсов со студентами и зачислениями
query = """
{
  courses {
    id
    title
    likes
    enrollments {
      id
      student {
        id
        name
        email
      }
    }
  }
}
"""

response = httpx.post(BASE, json={"query": query})
print(f"Status Code: {response.status_code}")
print(f"SQL Queries Count: {response.headers.get('X-SQL-Queries', 'N/A')}")
print("Response JSON:")
print(response.json())