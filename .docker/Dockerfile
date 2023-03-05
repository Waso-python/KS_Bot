# Определяем базовый образ
FROM python:3.10

# Устанавливаем рабочую директорию приложения в контейнере
WORKDIR /app

# Копируем файлы приложения в контейнер
COPY requirements.txt ./
COPY *.py ./
ADD .venv .

# Устанавливаем зависимости из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Запускаем приложение
CMD [ "python", "bot.py" ]
