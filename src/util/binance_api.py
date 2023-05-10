import pandas as pd
from time import time
from binance.client import Client

def _data_to_df(data: dict) -> pd.DataFrame:
    """
    Convert a Binance API response with price information to a Pandas Dataframe with the following columns:
    - Symbol: `str`
    - Timestamp: `pd.Timestamp`
    - Price: `float`
    """
    df = pd.DataFrame([data])                                   # create df from JSON document
    df = df.loc[:,['symbol', 'timestamp', 'price']]             # filter df for relevant columns
    df.columns = ['Symbol', 'Timestamp', 'Price']               # rename columns
    df.Price = df.Price.astype(float)                           # change column datatype
    df.Timestamp = pd.to_datetime(df.Timestamp, unit='s')       # change column datatype
    return df

def symbol_info(symbol: str) -> pd.DataFrame:
    """
    Get price information for a symbol from the Binance API as Pandas Dataframe
    """
    client = Client()
    symbol_data = client.get_symbol_ticker(symbol=symbol)
    symbol_data['timestamp'] = int(time())
    return _data_to_df(symbol_data)