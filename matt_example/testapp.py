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

csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')
df = pd.read_csv(StringIO(csv_string))
dates = df["Date"].values.tolist()
covid_levels = df["Covid Level"].values.tolist()

@app.route('/')
def about():
    return render_template("about.html", labels=dates, values=covid_levels)

if __name__ == "__main__":
    app.run()