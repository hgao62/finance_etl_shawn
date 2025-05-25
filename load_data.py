import pandas as pd
from sqlalchemy import create_engine

# Replace these with your actual credentials
DB_USER = "root"
DB_PASSWORD = "jiushiwo"
DB_NAME = "finance_etl"
DB_HOST = "localhost"  # Or another host if remote
DB_PORT = "3306"

# Create SQLAlchemy engine
ENGINE = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def save_df_to_db(
    df: pd.DataFrame,
    table_name: str,
    if_exists: str = "append",
    dtype=None,
) -> None:
    """
    Function to send a dataframe to SQL database.

    Args:
        df: DataFrame to be sent to the SQL database.
        table_name: Name of the table in the SQL database.
        if_exists: Action to take if the table already exists in the SQL database.
                   Options: "fail", "replace", "append" (default: "append").
        dtype: Dictionary of column names and data types to be used when creating the table (default: None).

    Returns:
        None. This function logs a note in the log file to confirm that data has been sent to the SQL database.
    """
    try:
        df.to_sql(
            name=table_name,
            con=ENGINE,
            if_exists=if_exists,
            index=False,
            dtype=dtype
        )
        print(f"[INFO] Data saved to `{table_name}` table.")
    except Exception as e:
        print(f"[ERROR] Failed to save to `{table_name}`: {e}")

