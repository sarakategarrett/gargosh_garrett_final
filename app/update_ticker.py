from app.db_connect import connect
import yfinance as yf


def post_ticker_prices():
    # call

def get_ticker():

def get_stock_price(symbol):
    ticker_yahoo = yf.Ticker(symbol)
    data = ticker_yahoo.history()
    last_quote = (data.tail(1)['Close'].iloc[0])
    return last_quote
