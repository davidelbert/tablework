# Tablework: Demonstration of an AI Agent, Natural Language Interface to PostgreSQL via Ollama + LangChain

This project ingests a CSV file with scientific metadata into a PostgreSQL database. It uses FastAPI to connect a AI agent and allow users to ask natural language questions and get results as real SQL queries.  Query results are returned as JSON or displayed in a Pandas dataframe in Jupyter.

---

## Features

- Demo ingests CSV with 175,000+ rows and multi-valued fields
- Agent-based, natural language query (e.g. "Find entries where MAT includes titanium")
- PostgreSQL-backed for broad applicability
- Ollama + LangChain-powered agent
- Jupyter notebook interface with Pandas output
- Supports pagination and approximate matching

---

## Requirements

- Docker + Docker Compose
- [Ollama](https://ollama.com) installed and running locally
- Python 3.10+ for optional Jupyter interface
- Jupyter (for notebook use)

---

## Project Structure

```
.
├── app/                  # FastAPI app with LangChain agent
│   └── ai_query.py       # Handles NL → SQL → result pipeline
├── db/                   # Database schema + CSV loader
│   ├── init.sql
│   └── load_data.py
├── data/                 # Put the CSV data file here
│   └── ner_abstracts_extracted_r1.csv
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
└── query_agent.ipynb     # Jupyter notebook interface
```

---

## Quickstart Instructions

### 1. Start Ollama with a model

In a terminal outside Docker:

```bash
ollama run llama3
```

Leave it running.

---

### 2. Start the Dockerized app

```bash
docker compose build
docker compose up
```

This initializes PostgreSQL and runs `init.sql`. Starts the FastAPI agent at http://localhost:8000

---

### 3. Load the CSV into the database

```bash
docker compose exec web python db/load_data.py
```

You should see a success message like:
```Rows inserted: 175661
```

---

### 4. Test the AI agent (terminal)

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show 10 entries where MAT includes Ti and DSC includes alloys"}'
```

Returns:
```json
{
  "query": "...",
  "sql": "...",
  "results": [...]
}
```

---

### 5. Use the Jupyter Notebook 
(probably the normal route since people don't like to write API calls all the time)

1. Open `query_agent.ipynb`
2. Run:

```python
ask_agent("Show entries where MAT includes aluminum, page 2")
```

Returns a nicely formatted Pandas DataFrame of results.

---

## Notes

- Array fields are searched using fuzzy matching via `ILIKE` and `unnest(...)`
- Only key columns (`index_id`, `title`, `doi`, `mat`, `dsc`) are returned by default
- Pagination is supported by adding “page N” to your prompt (each page = 10 rows)

---

## Possibilities

- Add a web-based chat UI or put something in the portal
- Export matched results to CSV or JSON
- Integrate full-text search on `abstract`
- Support saving prompt history

---

## Working Notes

- To reset the DB:
  ```bash
  docker compose down --volumes
  ```

- To rebuild:
  ```bash
  docker compose build
  docker compose up
  ```

- To enter Postgres manually:
  ```bash
  docker compose exec db psql -U postgres -d tablework
  ```


