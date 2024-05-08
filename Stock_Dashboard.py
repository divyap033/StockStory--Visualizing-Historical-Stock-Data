import requests
import pandas as pd
import matplotlib.pyplot as plt
import dash
from dash import html
from dash import dcc
import plotly.graph_objs as go
from flask import Flask, render_template
import plotly.graph_objs as go
import pandas as pd

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
    
if __name__ == "__main__":
    #stock_name = input("Enter stock name ")
    #start_date = input ("Enter start date in 'yyyy-mm-dd'  ")
    #end_date =input ("Enter end date in'yyyy-mm-dd'  ")
    stock_name = 'TSLA'  # Replace with the desired stock symbol
    start_date = '2022-01-01'  # Replace with the start date
    end_date = '2022-12-31'  # Replace with the end date

    stock_data = fetch_stock_data(stock_name, start_date, end_date)
    if stock_data:
        print(stock_data)  # Replace with code to display or process fetched data
        data = stock_data.get('results',[])

            # Create DataFrame
        df = pd.DataFrame(data)
        
        # Display the DataFrame
        print(df)
    
    #Data Analysis
        
        # Convert 't' (timestamp) to datetime
df['t'] = pd.to_datetime(df['t'], unit='ms')
# Plotting close price over time
plt.figure(figsize=(10, 6))
plt.plot(df['t'], df['c'], label='Close Price', color='blue')
plt.xlabel('Time')
plt.ylabel('Close Price')
plt.title('Stock Close Price Over Time')
plt.legend()
plt.show()

#Dash board
#http://127.0.0.1:8050/



app = dash.Dash(__name__)

# Assuming 'data' is your DataFrame containing the stock data

# Create a line chart
trace = go.Scatter(x=df['t'], y=df['c'], mode='lines', name='Close Price')
layout = go.Layout(title='Stock Close Price Over Time', xaxis=dict(title='Time'), yaxis=dict(title='Close Price'))
fig = go.Figure(data=[trace], layout=layout)

app.layout = html.Div(children=[
    html.H1(children='Stock Data Dashboard'),
    dcc.Graph(id='stock-graph', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)

#Using Flask

@app.route('/')
def index():
    # Convert 't' (timestamp) to datetime
    data['t'] = pd.to_datetime(df['t'], unit='ms')

    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['t'], y=df['c'], mode='lines', name='Close Price'))

    # Convert Plotly figure to JSON
    graphJSON = fig.to_json()

    return render_template('index.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
