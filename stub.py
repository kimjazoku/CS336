import psycopg2
import pandas as pd
import sys

user = 'stl71'

def query_to_dataframe(sql):
    conn = psycopg2.connect(
        dbname=user,
        user=user,
        password="",
        host="Postgres.cs.rutgers.edu",
        port="5432"
    )
    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]

    df = pd.DataFrame(rows, columns=colnames)

    cur.close()
    conn.close()

    return df

if len(sys.argv) == 1:
	pass
else:
	sql = sys.argv[1]

# sql = "SELECT as_of_year, agency_name FROM preliminary limit 1;"
df = query_to_dataframe(sql)
print(df.to_markdown(index=False))
