import psycopg2
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
import os

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

# PostgreSQL-Verbindungsparameter aus Umgebungsvariablen
db_params = {
    'dbname': os.getenv("db_name"),
    'user': os.getenv("db_user"),
    'password': os.getenv("db_password"),
    'host': os.getenv("db_host")
}

# Verbindung zur PostgreSQL-Datenbank herstellen und überprüfen
try:
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    print("Verbindung zur Datenbank erfolgreich hergestellt.")

    # SQL-Befehle zum Erstellen der Tabellen
    create_company_table = """
    CREATE TABLE IF NOT EXISTS Company (
        Ticker VARCHAR(10) PRIMARY KEY,
        Name VARCHAR(100) NOT NULL,
        Sector VARCHAR(50)
    );
    """

    create_company_information_table = """
    CREATE TABLE IF NOT EXISTS CompanyInformation (
        Ticker VARCHAR(10) PRIMARY KEY,
        Country VARCHAR(50),
        City VARCHAR(50),
        Industry VARCHAR(50),
        MarketCap BIGINT,
        FOREIGN KEY (Ticker) REFERENCES Company(Ticker)
    );
    """

    create_stock_price_table = """
    CREATE TABLE IF NOT EXISTS StockPrice (
        Ticker VARCHAR(10),
        Date DATE NOT NULL,
        Open DECIMAL(10, 2),
        High DECIMAL(10, 2),
        Low DECIMAL(10, 2),
        Close DECIMAL(10, 2),
        Volume BIGINT,
        Dividends DECIMAL(10, 2),
        Splits DECIMAL(10, 2),
        PRIMARY KEY (Ticker, Date),
        FOREIGN KEY (Ticker) REFERENCES Company(Ticker)
    );
    """

    create_currency_table = """
    CREATE TABLE IF NOT EXISTS Currency (
        Ticker VARCHAR(10) PRIMARY KEY,
        Name VARCHAR(100) NOT NULL
    );
    """

    create_currency_price_table = """
    CREATE TABLE IF NOT EXISTS CurrencyPrice (
        Ticker VARCHAR(10),
        Date DATE NOT NULL,
        Open DECIMAL(10, 5),
        High DECIMAL(10, 5),
        Low DECIMAL(10, 5),
        Close DECIMAL(10, 5),
        PRIMARY KEY (Ticker, Date),
        FOREIGN KEY (Ticker) REFERENCES Currency(Ticker)
    );
    """

    # Tabellen erstellen
    cur.execute(create_company_table)
    cur.execute(create_company_information_table)
    cur.execute(create_stock_price_table)
    cur.execute(create_currency_table)
    cur.execute(create_currency_price_table)

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    cur.close()
    conn.close()

    print("Tabellen erfolgreich erstellt.")
except Exception as e:
    print(f"Fehler beim Herstellen der Verbindung oder beim Erstellen der Tabellen: {e}")
