from langchain.llms import Ollama

llm = Ollama(model="llama3", base_url="http://host.docker.internal:11434")


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

    sql = llm.invoke(prompt)
    return {"query": nl_query, "sql": sql, "results": []}
