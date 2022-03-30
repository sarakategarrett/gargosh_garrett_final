from app import db, app
from app.db_connect import connect

def get_asset_classes():
    conn = connect()
    with conn.cursor() as cur:
        sql = f'SELECT asset_class_id, asset_class_name, allocation_percent FROM asset'
        cur.execute(sql)
        return cur.fetchall()

