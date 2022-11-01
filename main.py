from flask import Flask, render_template
import boto
import boto.s3.connection

import boto3
import pandas as pd
import sys
from io import StringIO

app = Flask(__name__)

access_key = 'AKIA2BUHV4R2RS54PBTY'
secret_key = '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'
conn = boto.connect_s3(
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key)

bucket2 = conn.get_bucket("mattdtest")
client = boto3.client('s3', aws_access_key_id = access_key,
                    aws_secret_access_key = secret_key)

bucket_name = 'mattdtest'
object_key = 'testdata.csv'
object_keys = []
object_keys.extend(["testdata.csv", "testdata_2.csv"])
dates_all = []
covid_levels_all = []
for x in object_keys:
    csv_obj = client.get_object(Bucket=bucket_name, Key=x)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    dates_all.append(df["Date"].values.tolist())
    covid_levels_all.append(df["Covid Level"].values.tolist())

@app.route('/')
def about():
    return render_template("index.html", labels_all=dates_all, values_all=covid_levels_all)

@app.route('/index.html')
def home_page():
    return render_template("index.html", labels_all=dates_all, values_all=covid_levels_all)

@app.route('/file_upload.html')
def file_page():
    return render_template("file_upload.html")

@app.route('/graphs_data.html')
def graph_page():
    return render_template("graphs_data.html")

@app.route('/history.html')
def history_page():
    return render_template("history.html")

if __name__ == "__main__":
    app.run(debug= True, port=5000)