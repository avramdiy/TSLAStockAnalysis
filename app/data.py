from flask import Flask, render_template_string
import pandas as pd
import os

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

if __name__ == "__main__":
    app.run(debug=True)
