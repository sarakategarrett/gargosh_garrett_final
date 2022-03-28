from app import db, app
from app.db_connect import connect

def get_asset():
    conn = connect()
    with conn.cursor() as cur:
        sql = f'SELECT id, name, date(date) as date from asset'
        cur.execute(sql)
        return cur.fetchall()