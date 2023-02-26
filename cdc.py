import pandas as pd

data = pd.read_csv("https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv")

data = data.loc[data['location_key'].isin(["US_NM_35028"])]
data = data[["date","new_confirmed"]]
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#    print(data)

#data = data.loc[data['location_key'].isin(["US_MA_25025"])]
#data = data[["date","new_confirmed"]]
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(data)