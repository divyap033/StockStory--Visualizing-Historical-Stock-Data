import requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)

def fetch_stock_data(stock_name, start_date, end_date):
    api_key = 'yfLyUv2Vg1df3kp2zRidY1jGSZNcE9Lt'  # Replace with your Polygon API key
    base_url = f'https://api.polygon.io/v2/aggs/ticker/{stock_name}/range/1/day/{start_date}/{end_date}?apiKey={api_key}'

    response = requests.get(base_url)
    if response.status_code == 200:
        stock_data = response.json()
        return stock_data
    else:
        print('Failed to fetch data')
        return None

@app.route('/')
def index():
    stock_name = 'TSLA'  # Replace with the desired stock symbol
    start_date = '2022-01-01'  # Replace with the start date
    end_date = '2022-12-31'  # Replace with the end date

    stock_data = fetch_stock_data(stock_name, start_date, end_date)
    if stock_data:
        data = stock_data.get('results', [])
        df = pd.DataFrame(data)
        df['t'] = pd.to_datetime(df['t'], unit='ms')
        
        plt.figure(figsize=(10, 6))
        plt.plot(df['t'], df['c'], label='Close Price', color='blue')
        plt.xlabel('Time')
        plt.ylabel('Close Price')
        plt.title('Stock Close Price Over Time')
        plt.legend()
        plt.savefig('static/plot.png')  # Save plot as a file in 'static' folder
        
        return render_template('index.html', plot_url='static/plot.png')

if __name__ == '__main__':
    app.run(debug=True)
