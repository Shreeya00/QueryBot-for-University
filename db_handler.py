import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def run_query(query: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)

    if query.strip().lower().startswith("select"):
        result = cursor.fetchall()
        columns = cursor.column_names
        return [dict(zip(columns, row)) for row in result]
    else:
        conn.commit()
        return [{"message": "Query executed successfully."}]
