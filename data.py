from fastapi import APIRouter, Query
from db.db_manager import get_sqlite_connection

router = APIRouter()

@router.get("/data")
def get_table_data(table: str = Query(..., description="Table name")):
    conn = get_sqlite_connection()
    cursor = conn.cursor()

    query = f"SELECT * FROM {table}"
    rows = cursor.execute(query).fetchall()

    conn.close()

    return [dict(row) for row in rows]
