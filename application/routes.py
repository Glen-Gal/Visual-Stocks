from application import app
from flask import render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import calendar

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

   #-------------------------------------- WeekDay-wise Total Volume

    # Extract the day of the week and store it in a new column 'WeekDay'
    df['WeekDay'] = df['Date'].dt.weekday

    # Group the data by weekday and calculate the sum of 'Volume'
    check = df.groupby('WeekDay')['Volume'].sum()

    # Create a dictionary to map numerical values to weekday labels
    weekday_mapping = {
        0: 'Monday',
        0.5: 'Monday, noon (12:00 PM)',
        1: 'Tuesday',
        1.5: 'Tuesday, noon (12:00 PM)',
        2: 'Wednesday',
        2.5: 'Wednesday, noon (12:00 PM)',
        3: 'Thursday',
        3.5: 'Thursday, noon (12:00 PM)',
        4: 'Friday'
    }

    # Map the 'WeekDay' values to weekday labels
    check.index = check.index.map(weekday_mapping)

    # Convert the 'check' series to a DataFrame with columns 'Weekday' and 'Volume'
    check_df = pd.DataFrame({'Weekday': check.index, 'Volume': check.values})

    # Create Plotly Line Chart for WeekDay-wise Total Volume with markers
    fig_weekday_line = px.line(check_df, x='Weekday', y='Volume',
                            labels={'Volume': 'Total Volume of Stocks Traded'},
                            height=400,
                            markers=True,  # Add markers
                            )

    # Set the layout
    fig_weekday_line.update_layout(
        xaxis_title='Weekday', 
        yaxis_title='Total Volume',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_weekday_line_json = json.dumps(fig_weekday_line, cls=plotly.utils.PlotlyJSONEncoder)

    #-------------------------------------- Month Total Volume
    # Assuming df is your DataFrame
    df['Month'] = df['Date'].dt.month

    # Analyzing based on Month and plotting total volume
    var = df.groupby('Month')['Volume'].sum() / 1e9  # Convert to billions

    # Convert the variable into a pandas DataFrame
    var = pd.DataFrame({'Month': var.index.map(lambda x: calendar.month_name[x]),
                        'Volume': var.values})

    # Create Plotly Line Chart for Month-wise Total Volume with markers
    fig_month_line = px.line(var, x='Month', y='Volume',
                            labels={'Volume': 'Total Volume of Stocks Traded'},
                            height=400,
                            markers=True,  # Add markers
                            )

    # Set the layout
    fig_month_line.update_layout(
        xaxis_title='Month',
        yaxis_title='Total Volume',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_month_line_json = json.dumps(fig_month_line, cls=plotly.utils.PlotlyJSONEncoder)

    #-------------------------------------- Year Total Volume
    # Assuming df is your DataFrame
    df['Year'] = df['Date'].dt.year

    # Group the data by year and calculate the sum of 'Volume'
    check = df.groupby('Year')['Volume'].sum()

    # Convert the 'check' series to a DataFrame with columns 'Year' and 'Volume'
    check_df = pd.DataFrame({'Year': check.index, 'Volume': check.values})

    # Create Plotly Line Chart for Year-wise Total Volume with markers
    fig_year_line = px.line(check_df, x='Year', y='Volume',
                            labels={'Volume': 'Total Volume of Stocks Traded'},
                            height=400,
                            markers=True,  # Add markers
                            )

    # Set the layout
    fig_year_line.update_layout(
        xaxis_title='Year',
        yaxis_title='Total Volume',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_year_line_json = json.dumps(fig_year_line, cls=plotly.utils.PlotlyJSONEncoder)

    #-------------------------------------- 5 days

    # Filter the DataFrame for the last five dates
    last_five_dates = df['Date'].nlargest(4)
    last_five_dates_data = df[df['Date'].isin(last_five_dates)]

    # Create Plotly Line Chart for Stock Price
    fig_stock = px.line(last_five_dates_data, x='Date', y='Close',
                        labels={'Close': 'Stock Price'},
                        height=400)

    # Set the layout
    fig_stock.update_layout(
        xaxis_title='Date',
        yaxis_title='Stock Price',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

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
    fig_6m.update_layout(
        xaxis_title='Date', 
        yaxis_title='Stock Price',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

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
    fig_1y.update_layout(
        xaxis_title='Date', 
        yaxis_title='Stock Price',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

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
    fig_5y.update_layout(
        xaxis_title='Date', 
        yaxis_title='Stock Price',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_5y_json = json.dumps(fig_5y, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    #-------------------------------------- Bar chart total volumes traded in a month
    # Group data by month and calculate total volume
    df['Month'] = df['Date'].dt.month
    monthly_volume = df.groupby('Month')['Volume'].sum()

    # Convert the variable into a pandas DataFrame
    var = pd.DataFrame({
        'Month': monthly_volume.index.map(lambda x: calendar.month_name[x]),
        'Volume': monthly_volume.values
    })


    # Sort the DataFrame by volume in ascending order
    var = var.sort_values(by='Volume', ascending=True)

    # Create Plotly Bar Chart for Monthly Volume
    fig_pie = px.bar(var, x='Volume', y='Month',
                    labels={'Volume': 'Total Volume of Stocks Traded'},
                    orientation='h',
                    height=400)

    # Set the layout
    fig_pie.update_layout(
        xaxis_title='Total Volume of Stocks Traded',
        yaxis_title='Month',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

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
    fig_max_volume_by_day.update_layout(
        xaxis_title='Day of the Week', 
        yaxis_title='Max Volume', 
        barmode='stack',
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_max_volume_by_day_json = json.dumps(fig_max_volume_by_day, cls=plotly.utils.PlotlyJSONEncoder)

    #-------------------------------------- New Chart (F)

    # Create Plotly Scatter Chart for Open Prices
    fig_new = px.line(df, x='Date', y='Open',
                        labels={'Open': 'Stock Open Price'},
                        height=400)

    # Set the layout
    fig_new.update_layout(
        xaxis_title='Date', 
        yaxis_title='Stock Open Price',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_new_json = json.dumps(fig_new, cls=plotly.utils.PlotlyJSONEncoder)

    #-------------------------------------- Scatter of Volume Chart (F)

    # Create polynomial features
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(df[['Adj Close']])

    # Fit a linear regression model
    reg = LinearRegression()
    reg.fit(X_poly, df['Volume'])

    # Predict the values using the regression model
    df['Volume_Pred'] = reg.predict(X_poly)

    # Create Plotly Scatter Plot for Volume and Polynomial Regression
    fig_scatter_poly = px.scatter(df, x='Adj Close', y='Volume', 
                                  labels={'Volume': 'Total Stock Volumes', 'Adj Close': 'Adjusted Close'},
                                  height=400)
    
    # Add the polynomial regression line
    fig_scatter_poly.add_trace(px.line(df, x='Adj Close', y='Volume_Pred').data[0])

    # Set the layout
    fig_scatter_poly.update_layout(
        xaxis_title='Adj Close',
        yaxis_title='Total Stock Volumes',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    # Set the line color to red
    fig_scatter_poly.update_traces(line=dict(color='red'))

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_scatter_json = json.dumps(fig_scatter_poly, cls=plotly.utils.PlotlyJSONEncoder)

    # ------------------------------- Max Stock Volume Traded(WeekDay)

    # Extract the day of the week and store it in a new column 'WeekDay'
    df['WeekDay'] = df['Date'].dt.weekday

    # Group the data by weekday and calculate the sum of 'Volume'
    check = df.groupby('WeekDay')['High'].max().reset_index()

    # Create a dictionary to map numerical values to weekday labels
    weekday_mapping = {
        0: 'Monday',
        0.5: 'Monday, noon (12:00 PM)',
        1: 'Tuesday',
        1.5: 'Tuesday, noon (12:00 PM)',
        2: 'Wednesday',
        2.5: 'Wednesday, noon (12:00 PM)',
        3: 'Thursday',
        3.5: 'Thursday, noon (12:00 PM)',
        4: 'Friday'
    }

    # Map the 'WeekDay' values to weekday labels
    check.index = check.index.map(weekday_mapping)

    # Create Plotly Bar Chart for Total Volume of Stocks Traded WeekDay-wise
    fig_weekday = px.bar(check, x=check.index, y='High',
                        labels={'High': 'Total Price of Stocks Traded'},
                        height=400)

    # Set the layout
    fig_weekday.update_layout(
        xaxis_title='Weekday', 
        yaxis_title='Max Price',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Convert the Plotly figure to JSON for rendering in HTML
    graph_weekday_json = json.dumps(fig_weekday, cls=plotly.utils.PlotlyJSONEncoder)


    # Include this in your render_template
    return render_template("layout.html", 
                           graphWeekdayJSON=graph_weekday_json, 
                           graphScatterJSON=graph_scatter_json, 
                           graphWeekdayLineJSON=graph_weekday_line_json,
                           graphMonthLineJSON=graph_month_line_json,
                           graphYearLineJSON=graph_year_line_json,
                           graphStockJSON=graph_stock_json, 
                           graph6mJSON=graph_6m_json,
                           graph1yJSON=graph_1y_json, 
                           graph5yJSON=graph_5y_json, 
                           graphPieJSON=graph_pie_json,
                           graphMaxVolumeByDayJSON=graph_max_volume_by_day_json, 
                           newGraphJSON=graph_new_json)