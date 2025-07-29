# Market-simulator

A python fincancial market simulator api that stores information in a postgres db in three tables: Users, Positions and TransactionHistory. The [yfinance](https://github.com/ranaroussi/yfinance) api wrapper is used to retrieve financial data from Yahoo Finance.

## Functionality

The following endpoints are available:
 - depositCash
 - withdrawCash
 - buyProduct
 - sellProduct
 - getHistory
 - getPositions


## Local Setup

1. [Install Postgres](https://jdbc.postgresql.org/download/)
2. Run `pipenv install` to install dependencies. See guide to [pipenv](https://pipenv.pypa.io/en/latest/installation.html)
3. Create a `config.ini` file in the root of the project in the following format, replacing as appropriate with the values used when setting up postgres:

```
[postgresql]
dbname=<YourDBName>
user=<YourUserName>
passwore=<YourPassword>
host = localhost
```

4. Run the `db_setup.py` file to create the tables.
5. Run `pipenv shell` to start the virtual environment.
6. Run `uvicorn main:app` to start the local server.

To run local tests use the command `python -m pytest`
