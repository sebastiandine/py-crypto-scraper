from setuptools import setup

setup(
   name='Crypto Scraping',
   version='1.0',
   install_requires=[
      'beautifulsoup4>=4.12.2',
      'lxml>=4.9.2',
      'selenium>=4.9.0',
      'pandas>=2.0.1',
      'python-binance>=1.0.17',
      'sqlalchemy>=2.0.12',
      'psycopg2>=2.9.6',
      'cryptography>=40.0.2'
      ]
)