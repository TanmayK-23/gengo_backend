import psycopg2
import time
import re
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return psycopg2.connect(db_url)
        
    return psycopg2.connect(
        host="localhost",
        database="legacy_db",
        user="tanmay",
        password=""   # or "password" if you set one
    )
def get_schema_info():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema = 'sales'
    ORDER BY table_name, ordinal_position
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    schema = {}
    for table, column in rows:
        schema.setdefault(table, []).append(column)

    return schema

def get_foreign_keys():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        tc.table_name, 
        kcu.column_name, 
        ccu.table_name AS foreign_table_name,
        ccu.column_name AS foreign_column_name 
    FROM 
        information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
          AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
          AND ccu.table_schema = tc.table_schema
    WHERE tc.table_schema = 'sales' AND tc.constraint_type = 'FOREIGN KEY';
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    relationships = []
    for row in rows:
        relationships.append(f"{row[0]}.{row[1]} → {row[2]}.{row[3]}")

    return relationships

def suggest_index(sql):
    match = re.search(r'where (.+)', sql, re.IGNORECASE)
    if match:
        cols = re.findall(r'(\w+)\s*=', match.group(1))
        if cols:
            return f"💡 Consider adding index on: {', '.join(cols)}"
    return None

def execute_read_only_query(sql):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Set the search path to the 'sales' schema first
    cur.execute("SET search_path TO sales, public;")

    start = time.time()
    cur.execute(sql)
    rows = cur.fetchall()
    end = time.time()

    execution_time = end - start
    columns = [desc[0] for desc in cur.description]

    suggestion = None
    if execution_time > 0.5:
        suggestion = suggest_index(sql)

    cur.close()
    conn.close()

    return rows, columns, execution_time, suggestion