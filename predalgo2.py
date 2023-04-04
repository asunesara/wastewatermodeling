import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout

# read data
df = pd.read_csv('Texas.csv')
# using the open price as the variable
df.head()
df = df['actuals.cases'].values
df = df.reshape(-1, 1)

# split data into training and testing sets
dataset_train = np.array(df[:int(df.shape[0] * 0.8)])
dataset_test = np.array(df[int(df.shape[0] * 0.8):])
# scale data between zero and one
scaler = MinMaxScaler(feature_range=(0, 1))
dataset_train = scaler.fit_transform(dataset_train)
dataset_test = scaler.transform(dataset_test)


# function creates dataset , append last 50 data points & convert to array
def create_dataset(df):
    x = []
    y = []
    for i in range(50, df.shape[0]):
        x.append(df[i - 50:i, 0])
        y.append(df[i, 0])
    x = np.array(x)
    y = np.array(y)
    return x, y


# creates dataset for train & test data points
x_train, y_train = create_dataset(dataset_train)
x_test, y_test = create_dataset(dataset_test)

# reshape into a 3D array to run through LSTM layer
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# build model
model = Sequential()
model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1], 1)))  # initialization
model.add(Dropout(0.2))
model.add(LSTM(units=96, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=96, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=96))
model.add(Dropout(0.2))
model.add(Dense(units=1))  # dense layer of 1  b/c we output one value

# reshape again for 3 dimensions
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# regression , adam updates network weights
model.compile(loss='mean_squared_error', optimizer='adam')

# save model , epoch means every cycle of training dataset
model.fit(x_train, y_train, epochs=70, batch_size=35)
model.save('prediction.h5')
model = load_model('prediction.h5')

# data visualization
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)
y_test_scaled = scaler.inverse_transform(y_test.reshape(-1, 1))

# building & showing graph

#fig, ax = plt.subplots(figsize=(16, 8))
#ax.plot(y_test_scaled, color='blue', label='Original')
#plt.plot(predictions, color='purple', label='Predicted')
#plt.legend()
#plt.show()
