from app import db, app
from app.db_connect import connect

def get_asset_classes():
    conn = connect()
    with conn.cursor() as cur:
        sql = f'SELECT asset_class_id, asset_class_name, allocation_percent FROM asset'
        cur.execute(sql)
        return cur.fetchall()

def get_tickers():
    conn = connect()
    with conn.cursor() as cur:
        sql = f'SELECT t.ticker_id, t.ticker_symbol, t.company_name, t.current_price, a.asset_class_id, a.asset_class_name' \
            f'from ticker t '\
            f'JOIN asset a ON a.asset_class_id=t.asset_class_id;'
        cur.execute(sql)
        return cur.fetchall()

