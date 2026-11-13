from sqlalchemy import text
from db import engine

with open("seed.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

with engine.begin() as conn:
    # Сначала очищаем таблицы, чтобы не было конфликтов уникальности
    conn.execute(text("DELETE FROM enrollments;"))
    conn.execute(text("DELETE FROM students;"))
    conn.execute(text("DELETE FROM courses;"))
    
    # Выполняем сидинг
    for statement in sql_script.split(";"):
        if statement.strip():
            conn.execute(text(statement))

print("Seed completed successfully!")