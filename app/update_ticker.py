from app.db_connect import connect
import yfinance as yf


def gat_tickers_only():
    conn = connect()
    with conn.cursor() as cur:
        sql = f'SELECT ticker_symbol' \
            f'from ticker'
        cur.execute(sql)
        return cur.fetchall()

def get_stock_price(symbol):
    ticker_yahoo = yf.Ticker(symbol)
    data = ticker_yahoo.history()
    last_quote = (data.tail(1)['Close'].iloc[0])
    return last_quote

def update_price(symbol, price):
    conn = connect()
    with conn.cursor() as cur:
        sql = f'UPDATE ticker SET current_price = {price} WHERE ticker_symbol like "{symbol}";'
        try:
            cur.execute(sql)
            conn.commit()
        except:
            print("Did not work.")

def post_ticker_prices():
    tickers = get_tickers_only()
    for ticker in tickers:
        symbol = ticker['ticker_symbol']
        if symbol == "CASH":
            price = 1
            update_price(symbol, price)
        else:
            price = get_stock_price(ticker['ticker_symbol'])
            print(f"{symbol} {price}")
            update_price(symbol, price)



