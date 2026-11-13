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










1. Активация виртуального окружения (.venv)
Bash
.venv\Scripts\activate
2. Установка зависимостей (если что-то не установлено)
Bash
pip install -r requirements.txt
3. Запуск сервера разработки (Uvicorn)
Оставь этот терминал открытым или запусти сервер, а для тестов открой соседнее окно терминала.

Bash
uvicorn main:app --reload
4. Команды для проверки и тестирования (в новом окне терминала с активированным .venv)
Проверка N+1 оптимизации (DataLoader):

Bash
python try_n_plus_1.py
(Должно вывести ровно SQL queries: 3 для обоих кейсов).

Проверка GraphQL мутации создания студента (с валидацией бонуса):
Если хочешь быстро протестировать через скрипт или просто открой в браузере http://localhost:8000/graphql и отправь мутацию из GraphiQL.

Проверка REST ошибок валидации (Бонус 1 — Problem Details):

Bash
python try_post.py N bad
5. Финальная отправка изменений на GitHub
Когда всё проверил и убедился, что всё работает идеально, зафиксируй изменения в Git:

Bash
git add .
git commit -m "Finalize Lab 8 with all bonus tasks, DataLoader, and README"
git push origin main
Всё! Проект полностью собран, протестирован, задокументирован и готов к защите преподавателю!