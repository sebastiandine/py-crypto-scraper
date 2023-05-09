from selenium import webdriver
from selenium.webdriver.remote.webdriver import BaseWebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from util.eth_util import scrape_eth_gas
from util.btc_util import scrape_btc_fee
from util.bsc_util import scrape_bsc_gas

from util.binance_api import symbol_info

from time import sleep, time
import sqlalchemy
import os

# setup selenium driver
driver_options = Options()
driver_options.add_argument('-headless')
geckodriver_service = Service("/tmp/geckodriver")
driver = webdriver.Firefox(options=driver_options, service=geckodriver_service)
driver.set_page_load_timeout(30)

# setup database connection
db_protocol = os.getenv('DB_PROTOCOL')
db_user = os.getenv('DB_USER')
db_pw = os.getenv('DB_PW')
db_host = os.getenv('DB_HOST')
db_port = int(os.getenv('DB_PORT'))
db_name = os.getenv('DB_NAME')
engine = sqlalchemy.create_engine('{0}://{1}:{2}@{3}:{4}/{5}'.format(db_protocol, db_user, db_pw, db_host, db_port, db_name))

# start scraping
print("Service started ...")
while True:
    iteration_start = int(time())
    feeScrapeFunction = [scrape_bsc_gas, scrape_eth_gas, scrape_btc_fee]
    priceSymbols = ["BNBUSDT", "ETHUSDT", "BTCUSDT"]
    for scrapeFee in feeScrapeFunction:
        try:
            scrapeFee(driver).to_sql('NetworkFees', engine, if_exists='append', index=False)
        except:
            pass
    for symbol in priceSymbols:
        try: 
            symbol_info(symbol).to_sql('AssetPrices', engine, if_exists='append', index=False)
        except:
            pass
    iteration_end = int(time())
    sleep_duration = 60 - (iteration_end - iteration_start)
    if sleep_duration > 0:
        sleep(sleep_duration)
