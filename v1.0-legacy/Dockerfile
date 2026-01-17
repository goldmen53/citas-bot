# Используем образ с Python
FROM python:3.11-slim

# Устанавливаем зависимости для Google Chrome и Pygame
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    libsdl2-mixer-2.0-0 \
    google-chrome-stable \
    && apt-get clean

# Устанавливаем библиотеки Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /app
WORKDIR /app

# Запускаем скрипт
CMD ["python", "main.py"]