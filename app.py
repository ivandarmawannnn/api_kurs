from flask import Flask, request, jsonify

import yfinance as yf
import sys
import datetime
import json

app = Flask(__name__)

@app.route('/get_kurs', methods=['GET'])

def get_exchange_rate():
    # Fetch historical data for the currency pair
    date = request.args.get('date')
    currency = request.args.get('currency')

    adjusted_date = adjust_to_friday(date)

    ticker = f"{currency}IDR=X"
    dateend = dayplusone(adjusted_date)
    data = yf.download(ticker, start=adjusted_date, end=dateend)
        # Get the exchange rate for the given date
    rate = data['Close'].iloc[0]
    rate = str(rate)
    rate = float(rate.split('\n')[1].split()[1].split('.')[0])        
    
    return jsonify({"rate": rate})

def dayplusone(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    dateend= date + datetime.timedelta(days=1)
    return dateend

def adjust_to_friday(date_str):
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    day_of_week = date.weekday()
    
    if day_of_week == 5:  # Saturday
        date -= datetime.timedelta(days=1)
    elif day_of_week == 6:  # Sunday
        date -= datetime.timedelta(days=2)
    
    return date.strftime("%Y-%m-%d")

if __name__ == '__main__':
    app.run(debug=True,port=8000)