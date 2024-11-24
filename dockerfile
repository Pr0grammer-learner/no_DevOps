# Используем официальный Python образ в качестве основы
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения в контейнер
COPY . /app
COPY templates /app/templates

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Устанавливаем переменную окружения для Python
ENV PYTHONPATH=/app

# Открываем порт для Flask
EXPOSE 5000

# Запуск приложения
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
