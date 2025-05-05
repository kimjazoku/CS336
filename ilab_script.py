#!/usr/bin/env python3
import os
import sys
import psycopg2
import pandas as pd
from getpass import getpass

user = 'ksd102'

def get_connection():
    # You can set these in your environment (e.g. export PGHOST=..., etc.)
    params = {
        "host":     os.getenv("PGHOST", "Postgres.cs.rutgers.edu"),
        "port":     os.getenv("PGPORT", "5432"),
        "dbname":   os.getenv("PGDATABASE", user),  # default DB = your user
        "user":     user,
        "password": "",
    }

    return psycopg2.connect(**params)


def query_to_dataframe(sql: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()
    return df


def main():
    # 1) Grab SQL from argv or from stdin
    if len(sys.argv) > 1:
        sql = sys.argv[1]
    else:
        sql = sys.stdin.read().strip()

    if not sql:
        print("❌ ERROR: No SQL query provided. Pass it as an argument or via stdin.")
        sys.exit(1)
    
    # 2) Execute and print results
    try:
        df = query_to_dataframe(sql)
        # You can switch to df.to_string() if you don’t want Markdown
        print(df.to_markdown(index=False))
    except Exception as e:
        print(f"❌ Query failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
