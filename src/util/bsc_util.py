from bs4 import BeautifulSoup
import pandas as pd
from time import time 
from selenium.webdriver.remote.webdriver import BaseWebDriver

def json_to_df(json: str) -> pd.DataFrame:
    """
    Convert scraped JSON to a comparable Pandas Datatype
    """
    df = pd.DataFrame([json])                                                                                               # create df from JSON document
    df = df.loc[:,['symbol', 'timestamp', 'lowGwei', 'avgGwei', 'highGwei', 'lowDuration', 'avgDuration', 'highDuration']]  # filter df for relevant columns
    df.columns = ['Symbol', 'Timestamp', 'slowFee', 'avgFee', 'fastFee', 'slowDuration', 'avgDuration', 'fastDuration']     # rename columns
    df.Timestamp = pd.to_datetime(df.Timestamp, unit='s')                                                                   # change column datatype
    return df

def parse_bsc_duration(text:str) -> int :
    """
    Parse transaction duration from a string of schema: "(5-10 secs)", by calculating the median value.

    Return the parsed values as duration in seconds.
    """
    dur_low = int(text[1:text.find('-')])
    dur_high = int(text[text.find('-')+1:text.find(' secs')])

    return (int((dur_high + dur_low) /2))

def scrape_bsc_gas(driver: BaseWebDriver):
    """
    Scrape the current gas information from `https://bscscan.com/gastracker`.

    # Parameters
    Selenium webdriver object (we cannot use the `request` library here since `https://bscscan.com/` detects
    the scraping attempt when we use it).

    # Return
    The result will be a dictionary with the following fields
    * `lowGwei`, `avgGwei`, `highGwei`
    * `lowDuration`, `avgDuration`, `highDuration`
    """

    driver.get("https://bscscan.com/gastracker")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    data = {"timestamp": int(time()), "symbol": "BSC"}

    divGasDataPanel = soup.select('div.row.text-center.mb-3') # this is how we search with and-concat of filters
    data["lowGwei"] = int(divGasDataPanel[0].find("span", {"id": "standardgas"}).text.replace(" Gwei", ""))
    data["avgGwei"] = int(divGasDataPanel[0].find("span", {"id": "fastgas"}).text.replace(" Gwei", ""))
    data["highGwei"] = int(divGasDataPanel[0].find("span", {"id": "rapidgas"}).text.replace(" Gwei", ""))

    durations = divGasDataPanel[0].find_all("div", {"class": "text-secondary"})
    data["lowDuration"] = parse_bsc_duration(durations[0].text)
    data["avgDuration"] = parse_bsc_duration(durations[1].text)
    data["highDuration"] = parse_bsc_duration(durations[2].text)

    return json_to_df(data)