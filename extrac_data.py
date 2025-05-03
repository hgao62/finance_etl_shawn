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

    print(hist)

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
    
    print(df)

    return df

get_stock_history("MSFT", "1mo", "1d")



def get_exchange_rate(from_currency: str, to_currency: str, period: str, interval: str) -> pd.DataFrame:
    """
    Download FX exchange rate data between two currencies using Yahoo Finance.

    Args:
        from_currency (str): Base currency (e.g., "USD").
        to_currency (str): Quote currency (e.g., "GBP").
        period (str): Data period (e.g., "1mo", "5d").
        interval (str): Data interval (e.g., "1d", "1h").

    Returns:
        pd.DataFrame: FX rate history with columns Date, Ticker, From Currency, To Currency, Open, High, Low, Close, Adj Close.
    """
    fx_rate_ticker = f"{from_currency}{to_currency}=X"
    fx_rates = yf.download(fx_rate_ticker, period=period, interval=interval)
    
    fx_rates.reset_index(inplace=True)
    fx_rates["Ticker"] = fx_rate_ticker
    fx_rates["From Currency"] = from_currency
    fx_rates["To Currency"] = to_currency

    print(fx_rates)
    return fx_rates



def get_stock_currency_code(stock: str) -> str:
    """
    Get the currency code in which a stock is traded.

    Args:
        stock (str): Ticker symbol of the stock (e.g., "AAPL", "SHOP.TO").

    Returns:
        str: Currency code (e.g., "USD", "CAD").
    """
    ticker = yf.Ticker(stock)
    currency = ticker.fast_info.get("currency", "N/A")

    print(f"Currency for {stock} is {currency}")
    return currency



def get_news(stock: str) -> pd.DataFrame:
    """
    Get recent news articles related to the given stock.

    Args:
        stock (str): Stock ticker symbol (e.g., "AAPL", "MSFT", "IAG.L").

    Returns:
        pd.DataFrame: News articles with columns like uuid, title, publisher, link, type, and stock.
    """
    ticker = yf.Ticker(stock)
    news_list = ticker.news

    if not news_list:
        print(f"No news found for {stock}.")
        return pd.DataFrame()

    df = pd.DataFrame(news_list)
    df["stock"] = stock

    # Optional: Reorder columns if you want a clean structure
    columns_to_keep = ["stock", "uuid", "title", "publisher", "link", "providerPublishTime", "type"]
    df = df[[col for col in columns_to_keep if col in df.columns]]

    print(df.head())  # Optional: show top 5 entries
    return df



