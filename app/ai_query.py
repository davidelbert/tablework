import ollama

# The model you want to use (must be installed locally via `ollama run llama3`, etc.)
OLLAMA_MODEL = "llama3"  # or "mistral", "gemma", etc.


def query_handler(nl_query: str):
    prompt = f"""
You are an assistant that translates natural language questions into SQL for a PostgreSQL database.

The table is named `entries` and has these columns:
- col1: TEXT
- col2: TEXT[] (a list of tags)
- col3: TEXT[] (another list of tags)

Convert the following question into an SQL query:

"{nl_query}"

Only return the SQL code, no explanation.
"""

    response = ollama.chat(
        model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}]
    )
    sql = response["message"]["content"]

    return {"query": nl_query, "sql": sql, "results": []}
