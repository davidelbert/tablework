import os
from pathlib import Path

files = {
    "README.md": "# Tablework\n\nNatural language querying for structured CSV data.",
    ".env": "POSTGRES_USER=postgres\nPOSTGRES_PASSWORD=postgres\nPOSTGRES_DB=tablework\nOPENAI_API_KEY=your_api_key",
    "Dockerfile": """
FROM python:3.11-slim

WORKDIR /app
COPY ./app /app/app
COPY ./db /app/db
COPY ./data /app/data
COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
    "docker-compose.yml": """
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: tablework
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    volumes:
      - .:/app

volumes:
  pgdata:
""",
    "app/main.py": """
from fastapi import FastAPI
from app.ai_query import query_handler

app = FastAPI()

@app.post("/query")
def query(input: dict):
    return query_handler(input["query"])
""",
    "app/ai_query.py": """
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def query_handler(nl_query: str):
    # This is a placeholder example
    sql = f"-- SQL translation of: {nl_query}"
    return {"query": nl_query, "sql": sql, "results": []}
""",
    "app/requirements.txt": "fastapi\nuvicorn\nopenai\npsycopg2-binary\n",
    "db/init.sql": """
CREATE TABLE IF NOT EXISTS entries (
    id SERIAL PRIMARY KEY,
    col1 TEXT,
    col2 TEXT[],
    col3 TEXT[]
);

CREATE INDEX IF NOT EXISTS col2_gin ON entries USING GIN (col2);
CREATE INDEX IF NOT EXISTS col3_gin ON entries USING GIN (col3);
""",
    "db/load_data.py": """
import csv
import os
import psycopg2

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="db"
)
cur = conn.cursor()

with open('data/your_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Add appropriate parsing and SQL insert here
        pass

conn.commit()
cur.close()
conn.close()
""",
    "data/.gitkeep": "",  # empty placeholder to keep folder
}

# Create files and folders
for path, content in files.items():
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

print("✅ Project structure created.")
