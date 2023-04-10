import pandas as pd
import numpy as np
from statistics import mean
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import Callback
#from plotly import graph_objs as go
import tensorflow as tf
import main



class TrainingCallback(Callback):
    def on_train_begin(self, logs=None):
        print("Starting training...")
        
    def on_epoch_begin(self, epoch, logs=None):
        print(f"Starting epoch {epoch}")
        #main.status = epoch
        #print(main.status)
    #def on_train_batch_begin(self, batch, logs=None):
        #print(f"Training: Starting batch {batch}")

    #def on_train_batch_end(self, batch, logs=None):
        #print(f"Training: Finished batch {batch}")
        
    #def on_epoch_end(self, epoch, logs=None):
        #print(f"Finished epoch {epoch}")
    def on_train_end(self, logs=None):
        print("Finished training")

# main.status
def generate_proj(data_df):
    df = data_df
    cases_data = df[1].values
    cases_data = cases_data.reshape((-1, 1))
    dates = df[0]

    # splitting data into training and testing sets
    # 80 percent
    split_percent = 0.80
    split = int(split_percent * len(cases_data))

    cases_train = cases_data[:split]
    cases_test = cases_data[split:]

    date_train = df[0][:split]
    date_test = df[0][split:]

    # timeseries generator helps manipulate data from a sequence to supervised data
    # look back data is the specifying the number of previous days to look back
    look_back = 15
    train_generator = TimeseriesGenerator(cases_train, cases_train, length=look_back, batch_size=20)
    test_generator = TimeseriesGenerator(cases_test, cases_test, length=look_back, batch_size=1)

    # random seed
    #tf.keras.utils.set_random_seed(2)

    # building LSTM
    model = Sequential()
    model.add(LSTM(units=50, activation='relu', stateful=False, input_shape=(look_back, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit_generator(train_generator, epochs=25, verbose=1, callbacks= [TrainingCallback()])

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
        last_date = df[0].values[-1]
        forecasted_dates = pd.date_range(last_date, periods=days_to_forecast+1, inclusive='right').strftime('%m/%d/%Y')
        return forecasted_dates

    #my_data = np.append(cases_data, forecast(days_to_forecast, model))
    og_cases = cases_data.tolist()
    new_cases = forecast(days_to_forecast, model).tolist()
    new_dates = forecast_dates(days_to_forecast).tolist()
    last_7_mean = mean(og_cases[-7:])
    #print(og_cases[-7:])
    #print(last_7_mean)
    avg_arr = [last_7_mean] * 7
    my_dates = np.append(dates, forecast_dates(days_to_forecast)).tolist()
    #print(my_dates[1].strftime('%m/%d/%Y'))

    upper = []
    lower = []
    for i in new_cases:
        upper.append(i + (i * .15))
        lower.append(i - (i * .15))

    results = [og_cases, new_cases, my_dates, upper, lower, avg_arr]
    print("New Cases")
    print(new_cases)
    return(results)
    #print(type(dates.tolist()[1]))
    '''
    forecast = forecast(days_to_forecast, model)
    forecast_dates = forecast_dates(days_to_forecast)
    # actual data values from csv file that i inputted for percent accuracy for the sake of validation
    af = [7902403, 7902627, 7902627, 7902627, 7910455, 7910788, 7914571, 7915047]
    print("actual", af)
    print("predicted", forecast)
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
        name='test Data')
    trace3 = go.Scatter(
        x=forecast_dates,
        y=forecast,
        mode='lines',
        name='Prediction')
    layout = go.Layout(
        title="Covid Cases",
        xaxis={'title': "Date"},
        yaxis={'title': "Cases"})
    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
    fig.show()
    # Percent Accuracy
    PA1 = 100 - abs((((af[1] - forecast[1]) / af[1]) * 100))
    PA2 = 100 - abs((((af[2] - forecast[2]) / af[2]) * 100))
    PA3 = 100 - abs((((af[3] - forecast[3]) / af[3]) * 100))
    PA4 = 100 - abs((((af[4] - forecast[4]) / af[4]) * 100))
    PA5 = 100 - abs((((af[5] - forecast[5]) / af[5]) * 100))
    PA6 = 100 - abs((((af[6] - forecast[6]) / af[6]) * 100))
    PA7 = 100 - abs((((af[7] - forecast[7]) / af[7]) * 100))
    print(PA1)
    print(PA2)
    print(PA3)
    print(PA4)
    print(PA5)
    print(PA6)
    print(PA7) '''