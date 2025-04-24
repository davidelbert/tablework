import os
import psycopg2
from langchain_community.llms import Ollama

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

When generating SQL:
1. Only return these columns: index_id, title, doi, mat, dsc
2. Never include "abstract" in the SELECT statement
3. Always include a LIMIT and OFFSET for pagination
   - Assume page size is 10
   - If the user mentions "page 2", OFFSET should be 10
   - "page 3" → OFFSET 20, and so on
4. For fuzzy matches in arrays, use:
   EXISTS (
       SELECT 1 FROM unnest(column_name) AS val WHERE val ILIKE '%value%'
   )

Example:
"Show page 1 of entries where MAT includes Ti" →
SELECT index_id, title, doi, mat, dsc FROM entries 
WHERE EXISTS (SELECT 1 FROM unnest(mat) AS val WHERE val ILIKE '%ti%') 
LIMIT 10 OFFSET 0;

Now, convert the following natural language request into SQL:

"{nl_query}"

Only return the SQL query. No explanation.
"""

    sql = llm.invoke(prompt).strip()

    if "```sql" in sql:
        sql = sql.split("```sql")[-1].split("```")[0].strip()
    elif "```" in sql:
        sql = sql.split("```")[1].split("```")[0].strip()

    print(" SQL:\n", sql)

    results = run_query(sql)

    return {"query": nl_query, "sql": sql, "results": results}
