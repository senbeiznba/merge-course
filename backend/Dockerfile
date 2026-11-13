FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей (если нужны для сборки)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Копирование и установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# Открытие порта для FastAPI
EXPOSE 8000

# Запуск приложения через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]