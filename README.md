# PyCryptoScraper
This project implements the scraping of network fees of various blockchains as well as the simultaneous prices of the networks' coins. It stores these datasets in a connected database.

It uses the following sites to scrape network fees:
- Bitcoin - https://privacypros.io/tools/bitcoin-fee-estimator
- Ethereum - https://etherscan.io/gastracker 
- Binance Smart Chain - https://bscscan.com/gastracker

For the coin prices in USD, it uses the [Binance API](https://www.binance.com/en/binance-api) resp. the Python package [python-binance](https://pypi.org/project/python-binance/), that wraps around this API.

Within the connected database, the project automatically creates two tables to
store the scraped data:
* `NetworkFees` holds the network fee data
* `AssetPrices` holds the coin price data

## How to connect a Database
The project relies on specific environment variables to establish a connection to a relational database and store the scraped data in that database. The following environment variables need to be set to establish a connection:

* `DB_PROTOCOL` - The vendor-specific protocol (incl. a potential driver) of the database
* `DB_USER` - The database user that should be used to interact with the database 
* `DB_PW` - The password of the database user `DB_USER`
* `DB_HOST` - host of the database
* `DB_PORT` - port of the host to communicate with the database
* `DB_NAME` - name of the database

You can either set those environment variables manually before you start the project, or you populate an `.env`-file with the required data inside the project directory.
You can find a template for such a file at `.env-template`.

## How to run locally
**Note:** The current state of the project expects [PostgreSQL](https://www.postgresql.org/) as the database system. If you want to switch to another database, you need to install a different driver for Python and adjust the environment variable `DB_PROTOCOL` accordingly.

Install dependencies
```
$py-crypto-scraper/> cd src && pip install .
```
Run (make sure that the required environment variable are set - either manually or via `.env`)
```
$py-crypto-scraper/src/> python3 main.py
```

## Build and run as Docker container
Build image from project
```
$py-crypto-scraper/> docker build -t myid/pyscraper .
```

Start container from new image and pass environment variables via `.env` file.
You can find a template for such a file at `.env-template`.
```
docker run -it --env-file .env myid/pyscrape
```

## How to extend/adjust
The project includes configuration for [VSCode development containers](https://code.visualstudio.com/docs/remote/containers) which should be the preffered environment to develop new features of the project. The container automatically sets up a whole Python development environment including the required geckodriver for the Selenium calls.

## Toolkit
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) - for data scraping
* [Selenium](https://pypi.org/project/selenium/) - as web driver for data scraping
* [SQLAlchemy](https://pypi.org/project/SQLAlchemy/) - for database interaction
* [Pandas](https://pypi.org/project/pandas/) - for structuring and transforming the data before storing it in the database
* [python-binance](https://pypi.org/project/python-binance/) - to interact with the Binance API
