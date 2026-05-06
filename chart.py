from fastapi import APIRouter
from db.db_manager import get_sqlite_connection
from mcp.mcp_store import mcp

router = APIRouter()

@router.get("/chart/config")
def get_chart_config():
    context = mcp.get_context()

    table = context["table"]
    x_axis = context["x_axis"]
    y_axis = context["y_axis"]
    chart_type = context["chart_type"]

    conn = get_sqlite_connection()
    cursor = conn.cursor()

    if not x_axis or not y_axis:
        rows = cursor.execute(f"SELECT * FROM {table}").fetchall()
        conn.close()
        return {
            "chart_type": chart_type,
            "data": [dict(row) for row in rows]
        }

    query = f"""
        SELECT {x_axis}, SUM({y_axis}) as value
        FROM {table}
        GROUP BY {x_axis}
    """

    rows = cursor.execute(query).fetchall()
    conn.close()

    return {
        "chart_type": chart_type,
        "x_axis": x_axis,
        "y_axis": y_axis,
        "data": [dict(row) for row in rows]
    }
