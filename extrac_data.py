import pandas as pd
import yfinance as yf

def get_stock_history(stock: str, period: str, interval: str) -> pd.DataFrame:
    """
    Pull stock history using Yahoo Finance API.

    Args:
        stock (str): Stock ticker symbol, e.g., "MSFT".
        period (str): Period of data to retrieve (e.g., "1mo", "3mo", "1y").
        interval (str): Data interval (e.g., "1d", "1h").

    Returns:
        pd.DataFrame: Stock history with columns like date, open, high, low, close, volume, dividends, and stock ticker.
    """
    ticker = yf.Ticker(stock)
    hist = ticker.history(period=period, interval=interval)
    hist.reset_index(inplace=True)
    hist['stock'] = stock
    return hist


import os

def get_stock_history_cached(stock: str, period: str, interval: str) -> pd.DataFrame:
    """
    Pull stock history with local cache to minimize API calls.

    Args:
        stock (str): Stock ticker symbol, e.g., "MSFT".
        period (str): Period of data to retrieve (e.g., "1mo", "3mo", "1y").
        interval (str): Data interval (e.g., "1d", "1h").

    Returns:
        pd.DataFrame: Cached or newly pulled stock history.
    """
    filename = f"cache_{stock}_{period}_{interval}.csv"

    if os.path.exists(filename):
        # If cached file exists, read from cache
        df = pd.read_csv(filename, parse_dates=['Date'])
    else:
        # Otherwise pull from API and cache it
        df = get_stock_history(stock, period, interval)
        df.to_csv(filename, index=False)

    return df
