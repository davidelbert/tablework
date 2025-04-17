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

success = 0
fail = 0

with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for i, row in enumerate(reader):
        try:
            if not row.get("Index") or not row["Index"].isdigit():
                print(f"⚠️ Skipping row {i}: Invalid or missing Index")
                fail += 1
                continue

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
            success += 1

        except Exception as e:
            fail += 1
            row_id = row.get("Index", f"row #{i}")
            print(f"❌ Skipped {row_id} due to error: {e}")

conn.commit()
cur.close()
conn.close()

print("✅ Data load complete.")
print(f"✅ Rows inserted: {success}")
print(f"❌ Rows skipped: {fail}")
