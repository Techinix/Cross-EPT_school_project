from flask import Flask, render_template_string
import csv
import threading
import time

app = Flask(__name__)

# Global variable to store the CSV data
csv_data = []

def read_csv_data():
    global csv_data
    with open('/home/techinix/Desktop/projet_ecole/cache/users_data_processed.csv', 'r') as file:
        reader = csv.reader(file)
        csv_data = list(reader)

def refresh_data():
    while True:
        read_csv_data()
        time.sleep(1)

# Route to render the web page
@app.route('/')
def index():
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CSV Data</title>
        <meta http-equiv="refresh" content="2">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
            }

            h1 {
                text-align: center;
                margin-bottom: 20px;
            }

            table {
                border-collapse: collapse;
                width: 100%;
            }

            th, td {
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }

            th {
                background-color: #f2f2f2;
            }

            tr:nth-child(even) {
                background-color: #f9f9f9;
            }

            tr:hover {
                background-color: #f5f5f5;
            }
        </style>
    </head>
    <body>
        <h1>Cross'EPT Leaderboard</h1>
        <table>
            {% for row in data %}
            <tr>
                {% for value in row %}
                <td>{{ value }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>


    '''
    return render_template_string(template, data=csv_data)

if __name__ == '__main__':
    # Start a separate thread for data refreshing
    refresh_thread = threading.Thread(target=refresh_data)
    refresh_thread.daemon = True
    refresh_thread.start()

    # Run the Flask application
    app.run(debug=True)

