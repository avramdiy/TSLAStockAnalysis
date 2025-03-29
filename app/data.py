from flask import Flask, render_template_string
import pandas as pd
import os
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

# Path to the CSV file
csv_path = r"C:\Users\Ev\Desktop\TRG Week 17\TSLA00-25.csv"

# Check if the file exists
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"File not found: {csv_path}")

@app.route("/")
def display_csv():
    # Load CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # Rename the "Price" column to "Date"
    df.rename(columns={"Price": "Date"}, inplace=True)

    # Remove the first two rows
    df = df.iloc[2:].reset_index(drop=True)

    # Convert DataFrame to HTML
    table_html = df.to_html(classes="table table-striped", index=False)

    # HTML template
    html_template = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSV Display</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-4">
            <h1 class="mb-4">CSV Data</h1>
            {{ table_html | safe }}
        </div>
    </body>
    </html>
    """

    return render_template_string(html_template, table_html=table_html)

@app.route("/chart")
def display_chart():
    # Load CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # Rename the "Price" column to "Date"
    df.rename(columns={"Price": "Date"}, inplace=True)

    # Remove the first two rows
    df = df.iloc[2:].reset_index(drop=True)

    # Ensure the "Date" column is in datetime format and filter rows from 2020 to 2025
    df["Date"] = pd.to_datetime(df["Date"])

    # Ensure "Close" is numeric and handle non-numeric values
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # Drop rows with missing or NaN values in "Close"
    df = df.dropna(subset=["Close"])

    # Filter rows between 2020 and 2025
    df = df[(df["Date"].dt.year >= 2020) & (df["Date"].dt.year <= 2025)]

    # Group by year and month, then calculate the average "Close" value
    df["YearMonth"] = df["Date"].dt.to_period("M")
    monthly_avg = df.groupby("YearMonth")["Close"].mean().reset_index()
    monthly_avg["YearMonth"] = monthly_avg["YearMonth"].dt.to_timestamp()

    # Create the line chart using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_avg["YearMonth"],
        y=monthly_avg["Close"],
        mode="lines+markers",
        name="Average Monthly Close"
    ))
    fig.update_layout(
        title="Average Monthly Close (2020-2025)",
        xaxis_title="Date",
        yaxis_title="Average Close",
        template="plotly_white"
    )

    # Convert Plotly figure to HTML
    chart_html = pio.to_html(fig, full_html=False)

    # HTML template for the chart page
    html_template = f"""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Line Chart</title>
    </head>
    <body>
        <div style="text-align: center; margin-top: 50px;">
            <h1>Line Chart: Average Monthly Close (2020-2025)</h1>
            {chart_html}
        </div>
    </body>
    </html>
    """

    return html_template


if __name__ == "__main__":
    app.run(debug=True)
