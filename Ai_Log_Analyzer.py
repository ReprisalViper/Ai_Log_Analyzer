# AI-Powered Log Analyzer (Docker-ready)

# 1. Import necessary libraries
import os
import re
import json
import psycopg2
import logging
import datetime
import pandas as pd
from sklearn.ensemble import IsolationForest
from flask import Flask, request, jsonify

# 2. Log Parser Function (basic example for Apache-style logs)
def parse_logs(log_path):
    pattern = re.compile(r'(?P<ip>\S+) - - \[(?P<date>.*?)\] "(?P<request>.*?)" (?P<status>\d{3}) (?P<size>\S+)')
    entries = []
    with open(log_path, 'r') as file:
        for line in file:
            match = pattern.match(line)
            if match:
                entries.append(match.groupdict())
    return pd.DataFrame(entries)

# 3. Anomaly Detection with Isolation Forest
def detect_anomalies(df):
    df['status'] = df['status'].astype(int)
    df['size'] = pd.to_numeric(df['size'], errors='coerce').fillna(0)
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly'] = model.fit_predict(df[['status', 'size']])
    return df

# 4. Save to PostgreSQL
def save_to_postgresql(df, conn_params):
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log_analysis (
            ip VARCHAR(50),
            date VARCHAR(50),
            request TEXT,
            status INT,
            size BIGINT,
            anomaly INT
        )
    """)
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO log_analysis (ip, date, request, status, size, anomaly)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['ip'], row['date'], row['request'], row['status'], row['size'], row['anomaly']))
    conn.commit()
    cursor.close()
    conn.close()

# 5. Flask API to upload and analyze logs
app = Flask(__name__)

@app.route('/upload-log', methods=['POST'])
def upload_log():
    log_file = request.files['logfile']
    filepath = f"/tmp/{log_file.filename}"
    log_file.save(filepath)

    df = parse_logs(filepath)
    df = detect_anomalies(df)

    conn_params = {
        'dbname': os.getenv('POSTGRES_DB', 'logdb'),
        'user': os.getenv('POSTGRES_USER', 'user'),
        'password': os.getenv('POSTGRES_PASSWORD', 'password'),
        'host': os.getenv('POSTGRES_HOST', 'db'),
        'port': os.getenv('POSTGRES_PORT', '5432')
    }
    save_to_postgresql(df, conn_params)
    return jsonify({"message": "Log file processed and saved to DB.", "anomalies": df[df['anomaly'] == -1].to_dict(orient='records')})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)