FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot/
COPY config.json ./

VOLUME ["/app/projects"]

ENV PYTHONPATH=/app

CMD ["python", "-m", "bot.main"]
