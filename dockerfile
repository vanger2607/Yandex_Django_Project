FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем весь проект
COPY yamozgi/ /app/

# По умолчанию запускаем Django сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
