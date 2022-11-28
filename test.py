from flask import Flask, render_template, request
import boto
import boto.s3.connection

import boto3
import pandas as pd
import sys
from io import StringIO
from werkzeug.utils import secure_filename

df = pd.read_csv('texas_clean.csv', header = None)
dates = (df.iloc[:,0]).values
cases = (df.iloc[:,1]).values

data_list = dates.reshape(1,dates.size)[0].tolist()
cases_list = cases.reshape(1,cases.size)[0].tolist()
#print(data_list)
#print(cases_list)

#df = df[df['Northern'].notna()]
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#    print(df)test


close_data = df.filter([1])
dataset = close_data.values
print(dataset)