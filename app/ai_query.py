import os
import psycopg2
from langchain_community.llms import Ollama

# Connect to your local Ollama server
llm = Ollama(model="llama3", base_url="http://host.docker.internal:11434")


def run_query(sql: str):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="db",
        )
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in rows]
        cur.close()
        conn.close()
        return result
    except Exception as e:
        return [{"error": str(e)}]


def query_handler(nl_query: str):
    prompt = f"""
You are an assistant that translates natural language questions into SQL for a PostgreSQL database.

The table is named `entries` and has these columns:
- index_id: INTEGER (unique identifier)
- abstract: TEXT
- pro, mat, smt, dsc, spl, cmt, apl: TEXT[] (lists of tags)
- title, doi, pii, journal: TEXT

To filter for values inside an array column like mat or dsc, use the syntax:
'value' = ANY(column_name)

Example:
"Find entries where MAT includes Ti" → 'Ti' = ANY(mat)

Convert the following question into an SQL query:

"{nl_query}"

Only return the SQL code, no explanation.
"""

    sql = llm.invoke(prompt).strip()

    # Remove markdown formatting if present
    if "```sql" in sql:
        sql = sql.split("```sql")[-1].split("```")[0].strip()
    elif "```" in sql:
        sql = sql.split("```")[1].split("```")[0].strip()

    print("🔍 Generated SQL:\n", sql)

    results = run_query(sql)

    return {"query": nl_query, "sql": sql, "results": results}
