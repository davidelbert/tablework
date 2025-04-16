FROM python:3.11-slim

WORKDIR /app
COPY ./app /app/app
COPY ./db /app/db
COPY ./data /app/data
COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
