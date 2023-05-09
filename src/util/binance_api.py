import pandas as pd
from time import time
from binance.client import Client

def json_to_df(json: str) -> pd.DataFrame:
    """
    Convert a Binance API JSON response with price information to a Pandas Dataframe with the following columns:
    - Symbol: `str`
    - Timestamp: `pd.Timestamp`
    - Price: `float`
    """
    df = pd.DataFrame([json])                                   # create df from JSON document
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
    return json_to_df(symbol_data)