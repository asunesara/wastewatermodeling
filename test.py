from flask import Flask, render_template, request
import boto
import boto.s3.connection

import boto3
import pandas as pd
import sys
from io import StringIO
from werkzeug.utils import secure_filename

df = pd.read_csv('bostondata.csv', skiprows=[0,2], usecols = ['Sample Date', 'Northern'])
df = df[df['Northern'].notna()]
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)
#def test_generate(filename):
#    dates_all = []
#    df = pd.read_csv(filename)
#    dates_all.append(df["actual.cases"].values.tolist())
#    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#         print(df)
#    print(dates_all)
#test