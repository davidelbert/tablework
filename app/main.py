from fastapi import FastAPI
from app.ai_query import query_handler

app = FastAPI()

@app.post("/query")
def query(input: dict):
    return query_handler(input["query"])
