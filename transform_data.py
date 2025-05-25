
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



def add_stock_returns(stock_history: pd.DataFrame) -> pd.DataFrame:
    """
    Adds daily and cumulative return columns to the stock history DataFrame.

    Args:
        stock_history (pd.DataFrame): DataFrame containing at least a 'close' column.

    Returns:
        pd.DataFrame: DataFrame with new columns 'daily_return' and 'cumulative_return'.
    """
    
    df = stock_history.copy()

    # Standardize column names (in case Date is capitalized)
    df.columns = [col.lower() for col in df.columns]

    if 'close' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'close' column")

    # Daily return = percentage change in close prices
    df['daily_return'] = df['close'].pct_change()

    # Cumulative return = product of (1 + daily_return), then subtract 1
    df['cumulative_return'] = (1 + df['daily_return']).cumprod() - 1

    return df



from extract_data import get_exchange_rate
# Add currency_code column using get_stock_currency_code
from extract_data import get_stock_currency_code



def standardize_price_to_usd(stock_history: pd.DataFrame) -> pd.DataFrame:
    """
    Convert local currency stock prices to USD by applying FX rate.

    Args:
        stock_history (pd.DataFrame): Data with 'currency_code' and 'close' columns.

    Returns:
        pd.DataFrame: With a new 'usd_close' column.
    """
    df = stock_history.copy()

    # Standardize column names (in case Date is capitalized)
    df.columns = [col.lower() for col in df.columns]

    # Check if currency column exists
    if 'currency_code' not in df.columns:
        if 'stock' in df.columns:
            ticker = df['stock'].iloc[0]
            df['currency_code'] = get_stock_currency_code(ticker)
        else:
            raise ValueError("Missing both 'currency_code' and 'stock' columns — cannot determine currency.")


    # Get local currency from the first row
    local_currency = df['currency_code'].iloc[0]

    # If already in USD, no conversion needed
    if local_currency == "USD":
        df['usd_close'] = df['close']
        print("Stock is already denominated in USD. No conversion needed.")
        return df

    # Get FX rate from local currency to USD
    fx_df = get_exchange_rate(local_currency, "USD", "1mo", "1d")
    fx_df.reset_index(inplace=True)

    # Flatten MultiIndex columns if present
    if isinstance(fx_df.columns, pd.MultiIndex):
        fx_df.columns = fx_df.columns.get_level_values(0)

    fx_df.columns = [col.lower() for col in fx_df.columns]

    # Ensure required columns exist
    if "close" not in fx_df.columns or "date" not in fx_df.columns:
        raise ValueError("FX data is missing 'close' or 'date' columns.")

    fx_df.rename(columns={"close": "fx_rate"}, inplace=True)

    # Normalize datetime (drop timezone)
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    fx_df["date"] = pd.to_datetime(fx_df["date"]).dt.tz_localize(None)

    # Merge
    df = pd.merge(df, fx_df[["date", "fx_rate"]], how="left", on="date")

    if "fx_rate" not in df.columns:
        raise ValueError("FX merge failed — 'fx_rate' column missing after merge.")


    # Calculate the USD close price
    df['usd_close'] = df['close'] * df['fx_rate']

    # Drop intermediate fx_rate column for clean output
    df.drop(columns=["fx_rate"], inplace=True)

    #print(df.head())  # Optional: Show the first few rows
    return df



def calculate_moving_average(stock_history: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """
    Calculate the moving average of the stock's close price.

    Args:
        stock_history (pd.DataFrame): DataFrame containing at least a 'close' column.
        window (int): Number of periods to calculate the moving average (default: 5).

    Returns:
        pd.DataFrame: Updated DataFrame with a new 'moving_average' column.
    """
    df = stock_history.copy()

    # Standardize column names (in case Date is capitalized)
    df.columns = [col.lower() for col in df.columns]

    # Check if the 'close' column exists
    if 'close' not in df.columns:
        raise ValueError("Input DataFrame must contain a 'close' column.")

    # Calculate the moving average
    df[f'moving_average_{window}'] = df['close'].rolling(window=window).mean()

    #print(df[[f'moving_average_{window}', 'close']].head())  # Optional: Preview the result
    return df


import pandas as pd

def get_top_bottom_days(stock_history: pd.DataFrame, ticker: str, top_n: int = 5) -> pd.DataFrame:
    """
    Get the top N and bottom N days by close price for a specific ticker.

    Args:
        stock_history (pd.DataFrame): DataFrame containing stock price history.
        ticker (str): Stock ticker to filter the data.
        top_n (int): Number of top and bottom days to return (default: 5).

    Returns:
        pd.DataFrame: Combined DataFrame of top N and bottom N days by close price.
    """
    df = stock_history.copy()

    # Standardize column names (in case Date is capitalized)
    df.columns = [col.lower() for col in df.columns]

    # Filter by ticker
    df = df[df['stock'] == ticker]

    # Check if 'close' column exists
    if 'close' not in df.columns:
        raise ValueError("The input DataFrame must contain a 'close' column.")

    # Get top N days by close price
    top_days = df.nlargest(top_n, 'close')

    # Get bottom N days by close price
    bottom_days = df.nsmallest(top_n, 'close')

    # Combine top and bottom days
    result = pd.concat([top_days, bottom_days]).sort_values(by='close', ascending=False).reset_index(drop=True)

    #print(result)  # Optional: Print the result for preview
    return result



def group_by_sector(stock_history: pd.DataFrame) -> pd.DataFrame:
    """
    Group stock data by sector and calculate average close price and volume.

    Args:
        stock_history (pd.DataFrame): DataFrame containing stock price history with 'sector', 'close', and 'volume' columns.

    Returns:
        pd.DataFrame: DataFrame with average close price and average volume grouped by sector.
    """
    df = stock_history.copy()

    # Standardize column names (in case Date is capitalized)
    df.columns = [col.lower() for col in df.columns]

    # Check if the required columns exist
    if not {'sector', 'close', 'volume'}.issubset(df.columns):
        raise ValueError("The input DataFrame must contain 'sector', 'close', and 'volume' columns.")

    # Group by sector and calculate the average close price and volume
    grouped_df = df.groupby('sector').agg(
        avg_close=('close', 'mean'),
        avg_volume=('volume', 'mean')
    ).reset_index()

    #print(grouped_df)  # Optional: Print for quick inspection
    return grouped_df
