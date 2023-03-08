# Определяем базовый образ
FROM python:3.10-slim

# Install Firebird 2.5 client library and dependencies
RUN apt-get update && \
    apt-get install -y libfbclient2 && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY requirements.txt ./



# Устанавливаем зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY *.py ./

# Запускаем приложение
CMD python bot.py
