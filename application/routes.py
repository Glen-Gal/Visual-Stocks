from application import app
from flask import render_template
import pandas as pd
import json
import plotly
import plotly.express as px
from datetime import datetime, timedelta

@app.route("/")
def index():
    # Load Dataset
    df = pd.read_csv('TSLA.csv')

    # Convert the Date column to DateTime object
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert 'Volume' to numeric
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')

    # Group data by year and calculate total volume
    df['Year'] = df['Date'].dt.year
    check = df.groupby('Year')['Volume'].sum()

    #-------------------------------------- All

    # Create Plotly Line Chart for Total Volume
    fig_volume = px.line(check, x=check.index, y='Volume',
                         labels={'Volume': 'Total Volume of Stocks Traded'},
                         height=400)

    # Set the layout
    fig_volume.update_layout(xaxis_title='Year', yaxis_title='Total Volume')

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_volume_json = json.dumps(fig_volume, cls=plotly.utils.PlotlyJSONEncoder)

    #-------------------------------------- 5 days

    # Filter the DataFrame for the last five dates
    last_five_dates = df['Date'].nlargest(4)
    last_five_dates_data = df[df['Date'].isin(last_five_dates)]

    # Create Plotly Line Chart for Stock Price
    fig_stock = px.line(last_five_dates_data, x='Date', y='Close',
                        labels={'Close': 'Stock Price'},
                        height=400)

    # Set the layout
    fig_stock.update_layout(xaxis_title='Date', yaxis_title='Stock Price')

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_stock_json = json.dumps(fig_stock, cls=plotly.utils.PlotlyJSONEncoder)

    #-------------------------------------- 6 months

    # Filter the DataFrame for the last 6 months
    start_date_6m = df['Date'].max() - pd.DateOffset(months=6)
    data_6m = df[df['Date'] >= start_date_6m]

    # Create Plotly Line Chart for Stock Price (6 months)
    fig_6m = px.line(data_6m, x='Date', y='Close',
                    labels={'Close': 'Stock Price'},
                    height=400)

    # Set the layout
    fig_6m.update_layout(xaxis_title='Date', yaxis_title='Stock Price')

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_6m_json = json.dumps(fig_6m, cls=plotly.utils.PlotlyJSONEncoder)

    #-------------------------------------- 1 year

    # Filter the DataFrame for the last year
    start_date_1y = df['Date'].max() - pd.DateOffset(years=1)
    data_1y = df[df['Date'] >= start_date_1y]

    # Create Plotly Line Chart for Stock Price (1 year)
    fig_1y = px.line(data_1y, x='Date', y='Close',
                     labels={'Close': 'Stock Price'},
                     height=400)

    # Set the layout
    fig_1y.update_layout(xaxis_title='Date', yaxis_title='Stock Price')

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_1y_json = json.dumps(fig_1y, cls=plotly.utils.PlotlyJSONEncoder)

    #-------------------------------------- 5 years

    # Filter the DataFrame for the last 5 years
    start_date_5y = df['Date'].max() - pd.DateOffset(years=5)
    data_5y = df[df['Date'] >= start_date_5y]

    # Create Plotly Line Chart for Stock Price (5 years)
    fig_5y = px.line(data_5y, x='Date', y='Close',
                     labels={'Close': 'Stock Price'},
                     height=400)

    # Set the layout
    fig_5y.update_layout(xaxis_title='Date', yaxis_title='Stock Price')

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_5y_json = json.dumps(fig_5y, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    #-------------------------------------- Pie Chart
    # Group data by month and calculate total volume
    df['Month'] = df['Date'].dt.month
    month_data = df.groupby('Month')['Volume'].sum().reset_index()

    # Create Plotly Pie Chart for Total Volume by Month
    fig_pie = px.pie(month_data, values='Volume', names='Month',
                     labels={'Volume': 'Total Volume of Stocks Traded'})

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_pie_json = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)
    
    #-------------------------------------- Max Volumes in a week
    
    # Convert the Date column to DateTime object
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert 'Volume' to numeric
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')

    # Define day names in the correct order (Monday to Sunday)
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Add 'DayOfWeek' column
    df['DayOfWeek'] = df['Date'].dt.day_name()

    # Calculate max volume for each day of the week
    max_volume_by_day = df.groupby('DayOfWeek')['Volume'].max().reset_index()

    # Map numeric day of the week to day names
    max_volume_by_day['DayOfWeek'] = max_volume_by_day['DayOfWeek'].map(dict(enumerate(day_names)))

    # Create Plotly Bar Chart for Max Volume by Day of the Week
    fig_max_volume_by_day = px.bar(max_volume_by_day, x='DayOfWeek', y='Volume',
                                    labels={'Volume': 'Max Volume of Stocks Traded'},
                                    height=400)

    # Set the layout
    fig_max_volume_by_day.update_layout(xaxis_title='Day of the Week', yaxis_title='Max Volume', barmode='stack',
                                        title='Max Volume by Day of the Week', showlegend=False)

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_max_volume_by_day_json = json.dumps(fig_max_volume_by_day, cls=plotly.utils.PlotlyJSONEncoder)

    # Include this in your render_template
    return render_template("layout.html", graphVolumeJSON=graph_volume_json, graphStockJSON=graph_stock_json, graph6mJSON=graph_6m_json,
                        graph1yJSON=graph_1y_json, graph5yJSON=graph_5y_json, graphPieJSON=graph_pie_json,
                        graphMaxVolumeByDayJSON=graph_max_volume_by_day_json)
