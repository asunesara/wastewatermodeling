from flask import Flask, render_template, request
import boto
import boto.s3.connection
import os
import math
from threading import Thread
import json
import boto3
import pandas as pd
import sys
from io import StringIO
from werkzeug.utils import secure_filename
from predalgo4 import *
from predalgo3 import *
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

global mean_7
mean_7 = 0
global status
status = 0
generated = False
proj = False
file_names = []
new_dates = []
new_covid = []
final_graph = []
bounds = []
upper_bounds = []
lower_bounds = []
def data_clear():
    mean_7= 0
    new_dates.clear()
    new_covid.clear()
    final_graph.clear()
    upper_bounds.clear()
    bounds.clear()
    lower_bounds.clear()
    global generated
    generated = False
    global proj
    proj = False
    global catch_error


def csv_to_df(file_name):
    csv_obj = client.get_object(Bucket=bucket_name, Key=file_name)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string), header=None)
    df = df.dropna()
    df = df[pd.to_numeric(df[1], errors='coerce').notnull()]
    df[1] = df[1].astype(float)
    return df

def new_generate(file_name):
    df = csv_to_df(file_name)
    dates = (df.iloc[:,0]).values
    cases = (df.iloc[:,1]).values
    data_list = dates.reshape(1,dates.size)[0].tolist()
    cases_list = cases.reshape(1,cases.size)[0].tolist()
    date_list = list(range(0,len(cases)))
    new_covid.append(cases_list)
    new_dates.append(data_list)
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

def new_proj(file_name):
    global mean_7
    df= csv_to_df(file_name)
    new_data = generate_proj(df)
    final_graph.clear()
    final_graph.append(new_data[2])
    new_covid.append(new_data[0])
    new_covid.append(new_data[1])
    final_graph.append(new_covid)
    upper_bounds = new_data[3]
    lower_bounds = new_data[4]
    mean_7 = new_data[5]
    bounds.append(upper_bounds)
    bounds.append(lower_bounds)

@app.route('/')
def about():
    return render_template("index.html")

@app.route('/index.html')
def home_page():
    return render_template("index.html")

@app.route('/testing.html')
def testing_page():
    batch = "N/A"
    test_str = "N/A"
    return render_template("testing.html", var = batch, str = test_str)

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
        try:
            new_generate(file_name)
            global generated
            generated = False
        except: 
            msg = "Error in csv - please check format of data."
            data_clear()
    return render_template("/file_upload.html",msg = msg)

@app.route('/update_graph', methods=['POST'])
def update_graph():
    #this will eventually call graces output first
    global generated
    generated = True
    global file_name
    new_update(file_name)
    #generate_data("testdata_2.csv")
    return render_template("graphs_data.html", data = final_graph, generated = generated, proj=proj, bounds = bounds,  mean_7 = mean_7)

@app.route('/resize', methods=['POST'])
def zoom_graph():
    global final_graph
    edit_dates = final_graph[0]
    edit_cases = final_graph[1][0]
    len_list = len(final_graph[0])
    len_list = math.floor(len_list * .2)
    edit_dates = edit_dates[len_list:]
    edit_cases = edit_cases[len_list:]
    final_graph[0] = edit_dates
    final_graph[1][0] = edit_cases
    return render_template("graphs_data.html", data = final_graph, generated = generated, proj=proj, bounds = bounds, mean_7 = mean_7)

@app.route('/update_proj', methods=['POST'])
def update_proj():
    global proj
    proj = True
    global file_name
    #t1 = Thread(target=new_proj(file_name))
    #t1.start()
    new_proj(file_name)
    return render_template("graphs_data.html", data = final_graph, generated=generated, proj=proj, bounds=bounds, mean_7 = mean_7)
    #return render_template("test_load.html")
    
@app.route('/download', methods=['POST'])
def download():
    filename = request.form["Download"]
    response = client.download_file(bucket_name, filename, filename)
    return render_template("history.html", name_list=file_names) 

@app.route('/graphs_data.html')
def graph_page():
    global generated
    return render_template("graphs_data.html", data = final_graph, generated = generated, proj=proj, bounds = bounds, mean_7 = mean_7)

@app.route('/history.html')
def history_page():
    return render_template("history.html", name_list=file_names)

@app.route('/status', methods=['GET'])
def getStatus():
    global status
    statusList = {'status':status}
    return json.dumps(statusList)

if __name__ == "__main__":
    app.run(debug= True, port=5000)
