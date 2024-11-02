# Базовый образ с Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем все файлы приложения
COPY . .

# Устанавливаем переменную окружения PYTHONPATH
ENV PYTHONPATH=/app

# Установка pytest для тестирования (только для CI/CD, не запускается в контейнере)
RUN pip install pytest

# Запуск Flask-сервера
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
