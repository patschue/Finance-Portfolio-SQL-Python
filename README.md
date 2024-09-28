# Python Financial Analysis, Portfolio Optimization and Risk

This repository showcases a series of Python scripts aimed at automating financial data management and analysis. It covers key areas in finance such as market data retrieval, portfolio optimization, risk assessment, and arbitrage detection. The project is designed to demonstrate practical competencies in Python for financial applications.

This repository will be updated from time to time.

## Features

- Market Data Retrieval: Download historical stock and FX data from multiple sources.
- Data Storage: Store the downloaded data in a PostgreSQL database for efficient retrieval and management.
- Portfolio Optimization: Calculate optimal portfolio weights using modern portfolio theory (e.g., Markowitz model).
- Portfolio Risk: Assess the risk associated with a portfolio, including measures like Value at Risk (VaR) and volatility.
- Arbitrage Detection: Identify potential arbitrage opportunities across different markets.

## Structure

- generate_db_tables.py: Script to generate PostgreSQL database tables.
- fill_db_tables.py.py: Script to download and store stock/FX data into a PostgreSQL database.
- portfolio_optimization.ipynb: Optimize portfolios based on given asset data and constraints.
- portfolio_risk.ipynb: Evaluate various portfolio risk metrics.
- arbitrage.ipynb: Analyze markets to find arbitrage opportunities.

## Database Setup

The PostgreSQL database credentials are stored in a .env file for security. This file includes sensitive information such as:

    db_host = your host
    db_name = your dbname
    db_user = your username
    db_password = your password

Make sure to create the .env file in the root directory of this project before running any scripts that interact with the database.

## Requirements

    Python 3.x
    PostgreSQL
    Required Python libraries are listed in requirements.txt

## Usage

After setting up the database and installing dependencies, you can start retrieving data, storing it in the database, and performing various financial analyses like portfolio optimization and arbitrage detection. Adjust parameters in the scripts according to your needs.
