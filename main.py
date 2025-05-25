from typing import List
from extract_data import get_stock_history, get_news, get_stock_currency_code
from transform_data import (
    add_stock_returns,
    standardize_price_to_usd,
    normalize_stock_data,
    calculate_moving_average,
)
from load_data import save_df_to_db


def run_pipeline(
    tickers: List[str],
    period: str = "1mo",
    interval: str = "1d",
) -> None:
    """
    End-to-end ETL pipeline that:
      - Downloads stock, financial, and news data
      - Transforms and enriches stock data
      - Saves everything to MySQL

    Args:
        tickers (List[str]): List of stock tickers to process
        period (str): Time range to pull from Yahoo Finance
        interval (str): Data frequency (e.g., "1d", "1h")
    """
    for ticker in tickers:
        print(f"\n📥 Processing {ticker}...")

        # Step 2.1: Extract data
        stock_history = get_stock_history(ticker, period, interval)
        # financial_data = get_stock_financials(ticker)
        news_data = get_news(ticker)

        # Step 2.2: Transform data
        stock_history = add_stock_returns(stock_history)
        stock_history = standardize_price_to_usd(stock_history)
        stock_history = normalize_stock_data(stock_history)
        stock_history = calculate_moving_average(stock_history)

        # Step 2.3: Load data into MySQL
        save_df_to_db(stock_history, "stock_history")
        save_df_to_db(news_data, "news")
        #save_df_to_db(financial_data, "financial")

        print(f"✅ Finished {ticker} ✅")

#pip install --upgrade yfinance


if __name__ == "__main__":
    tickers = ["MSFT", "AAPL", "SHOP.TO"]
    run_pipeline(tickers)


