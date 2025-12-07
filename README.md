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

## Docker setup

1. Ensure [Docker is istalled](https://www.docker.com/get-started/)
2. Edit the `config.ini` and `compose.yaml` replacing with your DB_NAME, DB_PASSWORD and DB_USERNAME.
3. Run `docker compose up --build`

## Manual Setup

1. [Install Postgres](https://jdbc.postgresql.org/download/)
2. Run `pipenv install` to install dependencies. See guide to [pipenv](https://pipenv.pypa.io/en/latest/installation.html)
3. Edit the `config.ini` file, replacing as appropriate with the values used when setting up postgres:

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
