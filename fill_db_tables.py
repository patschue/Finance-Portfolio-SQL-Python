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

# Verbindung zur PostgreSQL-Datenbank herstellen
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Liste der Unternehmensticker
lst_company = ["UBSG.SW", "UBS", "AAPL", "PFE", "AMZN", "META", "TSLA", "NVDA", "XOM", "MSFT", "KO"]
lst_currency = ["CHF=X", "EUR=X", "EURCHF=X"]

# Daten in die Tabelle Company laden
for comp in lst_company:
    company = yf.Ticker(comp).info
    ticker = company["symbol"]
    name = company.get("longName", "N/A")
    sector = company.get("sector", "N/A")

    cur.execute("INSERT INTO Company (Ticker, Name, Sector) VALUES (%s, %s, %s) ON CONFLICT (Ticker) DO NOTHING;",
                (ticker, name, sector))

# Daten in die Tabelle CompanyInformation laden
for comp in lst_company:
    company = yf.Ticker(comp).info
    ticker = company["symbol"]
    country = company.get("country", "N/A")
    city = company.get("city", "N/A")
    industry = company.get("industry", "N/A")
    marketCap = company.get("marketCap", 0)

    cur.execute("INSERT INTO CompanyInformation (Ticker, Country, City, Industry, MarketCap) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (Ticker) DO NOTHING;",
                (ticker, country, city, industry, marketCap))

# Daten in die Tabelle StockPrice laden
for comp in lst_company:
    ts = yf.Ticker(comp).history(period="5y")
    ticker = yf.Ticker(comp).info["symbol"]

    for date, row in ts.iterrows():
        cur.execute(
            "INSERT INTO StockPrice (Ticker, Date, Open, High, Low, Close, Volume, Dividends, Splits) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (Ticker, Date) DO NOTHING;",
            (
                ticker,
                date.date(),
                float(row['Open']),
                float(row['High']),
                float(row['Low']),
                float(row['Close']),
                int(row['Volume']),
                float(row['Dividends']),
                float(row['Stock Splits'])
            )
        )

for curr in lst_currency:
    currency = yf.Ticker(curr).info
    ticker = currency["symbol"]
    name = currency.get("longName", "N/A")

    cur.execute("INSERT INTO Currency (Ticker, Name) VALUES (%s, %s) ON CONFLICT (Ticker) DO NOTHING;",
                (ticker, name))
    
for curr in lst_currency:
    ts = yf.Ticker(curr).history(period="5y")
    ticker = yf.Ticker(curr).info["symbol"]

    for date, row in ts.iterrows():
        cur.execute(
            "INSERT INTO CurrencyPrice (Ticker, Date, Open, High, Low, Close) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (Ticker, Date) DO NOTHING;",
            (
                ticker,
                date.date(),
                float(row['Open']),
                float(row['High']),
                float(row['Low']),
                float(row['Close'])
            )
        )

# Änderungen speichern und Verbindung schließen
conn.commit()
cur.close()
conn.close()

print("Daten erfolgreich eingefügt.")
