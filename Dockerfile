FROM python:3.11-slim

WORKDIR /app

COPY ./app /app/app
COPY ./db /app/db
COPY ./data /app/data
COPY requirements.txt /app/requirements.txt

# 🔥 Pin and install correct ollama version before others
RUN pip install --upgrade pip && \
    pip install --no-cache-dir "ollama==0.1.8" && \
    pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
