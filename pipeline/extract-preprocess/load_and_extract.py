#!/usr/bin/env python3
import sys
import pandas as pd
from sqlalchemy import create_engine
import pathlib

def usage():
    print("Usage: load_and_extract.py <input_csv> <output_csv> <feature_sql_file>")
    sys.exit(1)

if len(sys.argv) != 4:
    usage()

input_csv = sys.argv[1]
output_csv = sys.argv[2]
feature_sql_file = sys.argv[3]

# Check files
if not pathlib.Path(input_csv).exists():
    raise SystemExit(f"Input CSV not found: {input_csv}")
if not pathlib.Path(feature_sql_file).exists():
    raise SystemExit(f"Feature SQL file not found: {feature_sql_file}")

# Load CSV with pandas
df = pd.read_csv(input_csv, parse_dates=True)

# Create SQLite DB
db_path = "/tmp/churn.db"
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})

# Write dataframe to 'raw'
df.to_sql("raw", con=engine, if_exists="replace", index=False)

# Read SQL file
with open(feature_sql_file, "r") as f:
    sql = f.read()

conn = engine.raw_connection()
cursor = conn.cursor()

try:
    # Split SQL statements properly
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    last_stmt = statements[-1] if statements else ""

    # Execute all non-SELECT statements
    for stmt in statements:
        if not stmt.lower().startswith("select"):
            cursor.execute(stmt)

    # Execute final SELECT
    if last_stmt.strip().lower().startswith("select"):
        df_out = pd.read_sql_query(last_stmt, con=engine)
        pathlib.Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
        df_out.to_csv(output_csv, index=False)
        print(f"Wrote features to {output_csv}")
    else:
        print("No final SELECT found in SQL file.")
except Exception as e:
    print("Error during SQL execution:", e)
finally:
    cursor.close()
    conn.close()
    engine.dispose()

