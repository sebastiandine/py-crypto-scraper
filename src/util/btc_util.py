from bs4 import BeautifulSoup
import pandas as pd
from time import time 
from selenium.webdriver.remote.webdriver import BaseWebDriver

def _data_to_df(data: dict) -> pd.DataFrame:
    """
    Convert scraped data to a comparable Pandas Datatype
    """
    df = pd.DataFrame([data])                                                                                               # create df from JSON document
    df = df.loc[:,['symbol', 'timestamp', 'lowSat', 'avgSat', 'highSat', 'lowDuration', 'avgDuration', 'highDuration']]     # filter df for relevant columns
    df.columns = ['Symbol', 'Timestamp', 'slowFee', 'avgFee', 'fastFee', 'slowDuration', 'avgDuration', 'fastDuration']     # rename columns
    df.Timestamp = pd.to_datetime(df.Timestamp, unit='s')                                                                   # change column datatype
    return df

def _parse_btc_duration(text: str) -> int:
    """
    Parse transaction duration from a string of schema: 
    "Next Block Fee: fee to have your transaction mined on the next block (10 minutes)."

    Return the parsed values as duration in seconds.
    """
    text_trimmed = text[text.find("(")+1:text.find(")")]
    if "seconds" in text_trimmed:
        return int(text_trimmed.replace(" seconds", ""))
    if "minutes" in text_trimmed:
        return (int(text_trimmed.replace(" minutes", "")) * 60)
    if "hours" in text_trimmed:
        return (int(text_trimmed.replace(" hours", "")) * 3600)
    if "hour" in text_trimmed:
        return (int(text_trimmed.replace(" hour", "")) * 3600)

def scrape_btc_fee(driver: BaseWebDriver) -> pd.DataFrame:
    """
    Scrape the current gas information from `https://privacypros.io/tools/bitcoin-fee-estimator/`.

    # Parameters
    Selenium webdriver object

    # Return
    The result will be a dictionary with the following fields
    * `lowSat`, `avgSat`, `highSat`
    * `lowDuration`, `avgDuration`, `highDuration`
    """
    driver.get("https://privacypros.io/tools/bitcoin-fee-estimator/")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    data = {"timestamp": int(time()), "symbol": "BTC"}

    fee_data = soup.find_all("span", {"class": "chart__fee-satoshi"})
    data["highSat"] = int(fee_data[0].text.replace("S/B", ""))
    data["avgSat"] = int(fee_data[1].text.replace("S/B", ""))
    data["lowSat"] = int(fee_data[2].text.replace("S/B", ""))

    durations = soup.find_all("td", {"class": "chart__fees-desc"})
    data["highDuration"] = _parse_btc_duration(durations[0].text)
    data["avgDuration"] = _parse_btc_duration(durations[1].text)
    data["lowDuration"] = _parse_btc_duration(durations[2].text)

    return _data_to_df(data)