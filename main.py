from flask import Flask, render_template, request
import boto
import boto.s3.connection
import os

import boto3
import pandas as pd
import sys
from io import StringIO
from werkzeug.utils import secure_filename
from predalgo4 import *
from sklearn.preprocessing import MinMaxScaler
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
file_name = ""

file_names = []
new_dates = []
new_covid = []
final_graph = []

def data_clear():
    new_dates.clear()
    new_covid.clear()
    final_graph.clear()


def csv_to_df(file_name):
    csv_obj = client.get_object(Bucket=bucket_name, Key=file_name)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string), header=None)
    return df

def new_generate_old(file_name):
    df = csv_to_df(file_name)
    close_data = df.filter(['actual.cases'])
    dataset = close_data.values
    data_list = dataset.reshape(1,dataset.size)[0].tolist()
    date_list = list(range(0,len(dataset)))
    new_covid.append(data_list)
    new_dates.append(date_list)
    final_graph.append(new_covid)
    final_graph.append(new_dates)

def new_generate(file_name):
    df = csv_to_df(file_name)
    dates = (df.iloc[:,0]).values
    cases = (df.iloc[:,1]).values
    data_list = dates.reshape(1,dates.size)[0].tolist()
    cases_list = cases.reshape(1,cases.size)[0].tolist()
    date_list = list(range(0,len(cases)))
    new_covid.append(cases_list)
    new_dates.append(date_list)
    final_graph.append(new_covid)
    final_graph.append(new_dates)


def new_update(file_name):
    df = csv_to_df(file_name)
    new_data = generate_results(df)
    new_dates.append(new_data[2])
    new_covid.append(new_data[0])
    final_graph.clear()
    final_graph.append(new_covid)
    final_graph.append(new_dates)


@app.route('/')
def about():
    return render_template("index.html")

@app.route('/index.html')
def home_page():
    return render_template("index.html")

@app.route('/file_upload.html')
def file_page():
    return render_template("file_upload.html")

@app.route('/upload',methods=['POST'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        split_tup = os.path.splitext(img.filename)
        file_extension = split_tup[1]
        if file_extension==".csv":
                filename = secure_filename(img.filename)
                try:
                    client.upload_fileobj(
                        img,
                        bucket_name,
                        img.filename,
                        ExtraArgs={"ACL":"public-read",
                                    "ContentType": img.content_type}
                    )
                except Exception as e:
                    print("Error", e)
                msg = "Upload Complete! "
        else:
            msg = "Incorrect File Format (.csv)"
            return render_template("/file_upload.html",msg = msg)
        data_clear()
        global file_name
        file_name = img.filename
        file_names.append(file_name)
        new_generate(file_name)
    return render_template("/file_upload.html",msg = msg)

@app.route('/update_graph', methods=['POST'])
def update_graph():
    #this will eventually call graces output first
    global file_name
    new_update(file_name)
    #generate_data("testdata_2.csv")
    return render_template("graphs_data.html", data = final_graph)
@app.route('/graphs_data.html')
def graph_page():
    return render_template("graphs_data.html", data = final_graph)

@app.route('/history.html')
def history_page():
    return render_template("history.html", name_list=file_names)

if __name__ == "__main__":
    app.run(debug= True, port=5000)