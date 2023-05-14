import os, csv
import pandas as pd
import talib
from flask import Flask, render_template, request
from patterns import candlestick_patterns
import yfinance as yf
from datetime import date

app = Flask(__name__)


@app.route('/snapshot')
def snapshot():
    with open('datasets/companies.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]
            data = yf.download(symbol, start="2020-01-01",  end=date.today())
            data.to_csv(f'datasets/daily/{symbol}.csv')

    return {
        "code": "success"
    }

@app.route("/")
def index():
    pattern = request.args.get('pattern', False)
    stocks = {}
    with open('datasets/companies.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}

    if pattern:
        datafiles = os.listdir('datasets/daily')
        for filename in datafiles:
            df = pd.read_csv(f'datasets/daily/{filename}')
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.')[0]

            try:
                result = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = result.tail(1).values[0]

                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
 
            except:
                pass

    return render_template("index.html", candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)