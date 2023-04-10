import pandas as pd
import numpy as np
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense, LSTM
from plotly import graph_objs as go
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('texas_clean.csv')

# scaler = MinMaxScaler(feature_range=(0, 1))
# df['actual.cases'] = scaler.fit_transform(df[['actual.cases']])

cases_data = df['Incidence'].values
cases_data = cases_data.reshape((-1, 1))
dates = df['Date']

# splitting data into training and testing sets
# 80 percent
split_percent = 0.80
split = int(split_percent * len(cases_data))

cases_train = cases_data[:split]
cases_test = cases_data[split:]

date_train = df['Date'][:split]
date_test = df['Date'][split:]

# timeseries generator helps manipulate data from a sequence to supervised data
# look back data is the specifying the number of previous days to look back
look_back = 15
train_generator = TimeseriesGenerator(cases_train, cases_train, length=look_back, batch_size=20)
test_generator = TimeseriesGenerator(cases_test, cases_test, length=look_back, batch_size=1)

# random seed
tf.keras.utils.set_random_seed(2)

# building LSTM
model = Sequential()
model.add(LSTM(units=50, activation='relu', stateful=False, input_shape=(look_back, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit_generator(train_generator, epochs=25, verbose=1)

# makes prediction
prediction = model.predict_generator(test_generator)

# reshaped data for graph
cases_train = cases_train.reshape((-1))
cases_test = cases_test.reshape((-1))
prediction = prediction.reshape((-1))
'''
# data visualization of predictions on top of training set and prior values
trace1 = go.Scatter(
    x=date_train,
    y=cases_train,
    mode='lines',
    name='Data')
trace2 = go.Scatter(
    x=date_test,
    y=prediction,
    mode='lines',
    name='Prediction')
trace3 = go.Scatter(
    x=date_test,
    y=cases_test,
    mode='lines',
    name='Actual Data')
layout = go.Layout(
    title="Covid Cases",
    xaxis={'title': "Date"},
    yaxis={'title': "Cases"})
fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
fig.show()'''
cases_data = cases_data.reshape((-1))

# implementing the forecasting
# forecast 7 days in the future
days_to_forecast = 7


# functions to help forecasting by manipulating the data
def forecast(days_to_forecast, model):
    prediction_list = cases_data[-look_back:]

    for i in range(days_to_forecast):
        x = prediction_list[-look_back:]
        x = x.reshape((1, look_back, 1))
        out = model.predict(x)[0][0]  # prediction is made
        prediction_list = np.append(prediction_list, out)  # forecast prediction is then appended to prediction list
    prediction_list = prediction_list[look_back - 1:]  # list of forecast predictions is finalized

    return prediction_list


def forecast_dates(days_to_forecast):
    last_date = df['Date'].values[-1]
    forecasted_dates = pd.date_range(last_date, periods=days_to_forecast + 1).tolist()
    return forecasted_dates


forecast = forecast(days_to_forecast, model)
forecast_dates = forecast_dates(days_to_forecast)

# outputting upper and lower bound uncertainty
f = []
fifteen = []
upper_bound = []
lower_bound = []
for i in forecast:
    f.append(i)
    x = (i / 100) * 15
    fifteen.append(x)
# print(f)
# print(fifteen)
ub = np.add(f, fifteen)
upper_bound.append(ub)
print("upper bound",*upper_bound)
lb = np.subtract(f, fifteen)
lower_bound.append(lb)
print("lower bound",*lower_bound)


# actual data values from csv file for validation
# af = [7902403, 7902627, 7902627, 7902627, 7910455, 7910788, 7914571, 7915047]
# print("actual", af)
# print("predicted", forecast)

# data visualization of predictions as well as testing data
trace1 = go.Scatter(
    x=date_train,
    y=cases_train,
    mode='lines',
    name='Data')
trace2 = go.Scatter(
    x=date_test,
    y=cases_test,
    mode='lines',
    name='Test Data')
trace3 = go.Scatter(
    x=forecast_dates,
    y=forecast,
    mode='lines',
    name='Prediction')
trace4 = go.Scatter(
    x=forecast_dates,
    y=upper_bound,
    mode='lines',
    name='Upper Bound Uncertainty')
trace5 = go.Scatter(
    x=forecast_dates,
    y=lower_bound,
    mode='lines',
    name='Lower Bound Uncertainty')
layout = go.Layout(
    title="Wastewater Incidence",
    xaxis={'title': "Date"},
    yaxis={'title': "Wastewater"})

fig = go.Figure(data=[trace1, trace2, trace3, trace4, trace5], layout=layout)
fig.show()