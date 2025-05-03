import pandas as pd

def normalize_stock_data(stock_history: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize stock data by rounding price columns to 2 decimals and renaming 'date' column to 'trade_date'.

    Args:
        stock_history (pd.DataFrame): Raw stock history data.

    Returns:
        pd.DataFrame: Cleaned and formatted stock data.
    """
    df = stock_history.copy()

    # Standardize column names (in case Date is capitalized)
    df.columns = [col.lower() for col in df.columns]

    # Rename 'date' to 'trade_date'
    if 'date' in df.columns:
        df.rename(columns={"date": "trade_date"}, inplace=True)

    # Round prices to 2 decimal places
    for col in ["open", "high", "low", "close"]:
        if col in df.columns:
            df[col] = df[col].round(2)

    return df
