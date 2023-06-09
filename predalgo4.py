from flask import Flask, render_template, request
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import Callback
import math
from sklearn.preprocessing import MinMaxScaler


class TrainingCallback(Callback):
    def on_train_begin(self, logs=None):
        print("Starting training...")
        
    def on_epoch_begin(self, epoch, logs=None):
        print(f"Starting epoch {epoch}")
    def on_train_batch_begin(self, batch, logs=None):
        print(f"Training: Starting batch {batch}")

    def on_train_batch_end(self, batch, logs=None):
        print(f"Training: Finished batch {batch}")
        
    def on_epoch_end(self, epoch, logs=None):
        print(f"Finished epoch {epoch}")
        return render_template("/testing.html", var=epoch)
    def on_train_end(self, logs=None):
        print("Finished training")


def generate_results(data):

    #  Plotting date vs the case
    # data.plot('Date', 'actual.cases', color="red")
    # plt.show()
    # Extract only top 60 rows to make the plot a little clearer
    # new_data = data.head(60)
    #  Plotting date vs the close  market stock price
    # new_data.plot('Date', 'actual.cases', color="green")

    # 1. defining variable
    #close_data = data.filter(['actual.cases'])

    # 2. Convert the data into array for easy evaluation
   # dataset = close_data.values
    close_data = data.filter([1])
    dataset = close_data.values
    #plt.show()
    # 3. Scale the data to make all values between 0 and 1
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    # 4. Creating training data size - using 70% of the data
    training_data_len = math.ceil(len(dataset) * .7)
    train_data = scaled_data[0:training_data_len, :]

    # 5. Separating the data into x and y data
    x_train_data = []
    y_train_data = []
    for i in range(60, len(train_data)):
        x_train_data = list(x_train_data)
        y_train_data = list(y_train_data)
        x_train_data.append(train_data[i - 60:i, 0])
        y_train_data.append(train_data[i, 0])

    # 6. Converting the training x and y values to numpy arrays
    x_train_data1, y_train_data1 = np.array(x_train_data), np.array(y_train_data)

    # 7. Reshaping training x and y data to make the calculations easier
    x_train_data2 = np.reshape(x_train_data1, (x_train_data1.shape[0], x_train_data1.shape[1], 1))

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train_data2.shape[1], 1)))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train_data2, y_train_data1, batch_size=1, epochs=2, callbacks= [TrainingCallback()])

    # 1. Creating a dataset for testing
    test_data = scaled_data[training_data_len - 60:, :]
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i - 60:i, 0])

    # 2.  Convert the values into arrays for easier computation
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    # 3. Making predictions on the testing data
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    #scores = model.evaluate(y_test, predictions)
    #LSTM_accuracy = scores[1]*100
    #print(LSTM_accuracy)

    #print('Test accuracy: ', scores[1]*100, '%')
    # print(predictions)
    # print(y_test)
    #RMSE = np.sqrt(np.mean(((predictions - y_test) ** 2)))
    # print(RMSE)
    #RMSE = RMSE/1000000
    #print(RMSE)


    train = data[:training_data_len]
    valid = data[training_data_len:]

    valid['Predictions'] = predictions
    prediction_list = predictions.reshape(1,predictions.size)[0].tolist()
    date_range = list(range(0,len(dataset)))
    date_range2 = list(range(training_data_len, len(dataset)))
    
    results = [prediction_list, date_range, date_range2]
    return results
#fig, ax = plt.subplots(figsize=(16, 8))
#plt.title('Covid cases prediction Model')
#plt.xlabel('Date')
#plt.ylabel('actual.cases')


#plt.plot(train['actual.cases'], color='purple')
#plt.plot(valid['Predictions'], color = "pink")
#plt.plot(valid['actual.cases'], color = "yellow")
##print(type(valid['actual.cases']))
##print(train['actual.cases'])
#plt.legend(['Train', 'Validation', 'Predictions'], loc='upper left')

#plt.show()
