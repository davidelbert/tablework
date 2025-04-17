import csv
import os
import psycopg2

CSV_PATH = "data/ner_abstracts_extracted_r1.csv"


def parse_list(cell):
    if not cell:
        return []
    return [item.strip() for item in cell.split(";")]


conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="db",
)

cur = conn.cursor()

with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        try:
            cur.execute(
                """
                INSERT INTO entries (
                    index_id, abstract, pro, mat, smt, dsc, spl, cmt, apl,
                    title, doi, pii, journal
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (index_id) DO NOTHING;
            """,
                (
                    int(row["Index"]),
                    row["Abstract_x"],
                    parse_list(row["PRO"]),
                    parse_list(row["MAT"]),
                    parse_list(row["SMT"]),
                    parse_list(row["DSC"]),
                    parse_list(row["SPL"]),
                    parse_list(row["CMT"]),
                    parse_list(row["APL"]),
                    row["title"],
                    row["doi"],
                    row["pii"],
                    row["journal"],
                ),
            )
        except Exception as e:
            print(f"❌ Skipped row {row['Index']} due to error: {e}")

conn.commit()
cur.close()
conn.close()
print("✅ Data load complete.")
