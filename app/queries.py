from app.db import get_conn

VIEWS = {
    "part_tick": "v_ohlc_15min"
}

def fetch_rows(metric: str):
    sql = f"SELECT * FROM {VIEWS[metric]}"
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            cols = [col.name for col in cur.description]
            rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    return rows
