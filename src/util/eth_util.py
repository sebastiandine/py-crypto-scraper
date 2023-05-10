from typing import Tuple
import pandas as pd
from bs4 import BeautifulSoup
from time import time 
from selenium.webdriver.remote.webdriver import BaseWebDriver

def _data_to_df(data: dict) -> pd.DataFrame:
    """
    Convert scraped data to a comparable Pandas Datatype
    """
    df = pd.DataFrame([data])                                                                                               # create df from JSON document
    df = df.loc[:,['symbol', 'timestamp', 'lowGwei', 'avgGwei', 'highGwei', 'lowDuration', 'avgDuration', 'highDuration']]  # filter df for relevant columns
    df.columns = ['Symbol', 'Timestamp', 'slowFee', 'avgFee', 'fastFee', 'slowDuration', 'avgDuration', 'fastDuration']     # rename columns
    df.Timestamp = pd.to_datetime(df.Timestamp, unit='s')                                                                   # change column datatype
    return df

def _parse_eth_price_duration(text:str) -> Tuple[float,int] :
    """
    Parse price and transaction duration from a string of schema: "$1.53 | ~ 3 mins: 0 secs".

    Return the parsed values as a tuple:
     - Price in USD as float
     - Duration in seconds as int
    """
    usd = float(text[2:text.find('|')-1])
    dur_txt = text[text.find('~')+2:].replace(' mins: ','-').replace(' secs','')    # convert to "<min>:<sec>"
    dur_min = int(dur_txt[:dur_txt.find('-')]) * 60 if "mins" in text else 0        # edge case no mins
    dur_sec = int(dur_txt[dur_txt.find('-')+1:])

    return(usd, dur_min+dur_sec)

def scrape_eth_gas(driver: BaseWebDriver) -> pd.DataFrame:
    """
    Scrape the current gas information from `https://etherscan.io/gastracker`.

    # Parameters
    Selenium webdriver object (we cannot use the `request` library here since `https://etherscan.io` detects
    the scraping attempt when we use it).

    # Return
    The result will be a dictionary with the following fields
    * `lowGwei`, `avgGwei`, `highGwei`
    * `lowUsd`, `avgUsd`, `highUsd`
    * `lowDuration`, `avgDuration`, `highDuration`
    """

    driver.get("https://etherscan.io/gastracker")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    data = {"timestamp": int(time()), "symbol": "ETH"}

    divLowPrice = soup.find("div", {"id": "divLowPrice"})
    data["lowGwei"] = int(divLowPrice.find("span", {"id": "ContentPlaceHolder1_ltGasPrice"}).text)
    divLowUsdDur = divLowPrice.find_all("div", {"class": "text-muted"})
    data["lowUsd"], data["lowDuration"] = _parse_eth_price_duration(divLowUsdDur[1].text)

    divAvgPrice = soup.find("div", {"id": "divAvgPrice"})
    data["avgGwei"] = int(divAvgPrice.find("span", {"id": "spanAvgPrice"}).text)
    divAvgUsdDur = divAvgPrice.find_all("div", {"class": "text-muted"})
    data["avgUsd"], data["avgDuration"] = _parse_eth_price_duration(divAvgUsdDur[1].text)

    divHighPrice = soup.find("div", {"id": "divHighPrice"})
    data["highGwei"] = int(divHighPrice.find("span", {"id": "spanHighPrice"}).text)
    divHighUsdDur = divHighPrice.find_all("div", {"class": "text-muted"})
    data["highUsd"], data["highDuration"] = _parse_eth_price_duration(divHighUsdDur[1].text)

    return _data_to_df(data)