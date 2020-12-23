## Written by Ricardo Valdez                                                                     
# City College of New York, CUNY 
# Date: October 18, 2020
# --------------------------------------------------------------------------
# | Project -  Zoom Stock Prediction                                       |
# --------------------------------------------------------------------------
# Sanjidah Wahid
# ee59837_16
#
# With an ANN, predict the next day closing price movement for Google stocks.
# Use the following 6 technical indicators as inputs for your ANN:
#     - Simple moving average (SMA)
#     - Exponential moving average (EMA)
#     - Momentum
#     - Bollinger bands (BB)
#     - William's %R
#     - Rate of change (ROC)
#     

import numpy as np
import pandas as pd
import time
from tensorflow import keras

def print_weights(weights):
    print('\n******* WEIGHTS OF ANN *******\n') 
    for i in range(int(len(weights)/2)):
        print('Weights W%d:\n' %(i), weights[i*2])
        print('Bias b%d:\n' %(i), weights[(i*2)+1])

#%% DATA EXTRACTION
historical_data_file = 'ZM.csv'

## load the historical stock data 
df = pd.read_csv(historical_data_file)

## keep only the closing prices 
df = df[['Close']]
short_window = 5
long_window = 25

## calculate the Simple Moving Average and add it to a new column in df;
## rolling means moving window starting from the current entry and 
## the last 5 days (open df in Variable explorer ad see the values)
df['SMA'] = df.rolling(short_window).mean()

## calculate the Exponential Moving Average and add it 
## to a new column in df;
## ewm means exponential moving average
df['EMA'] = df['Close'].ewm(span=long_window).mean()

## calculate the Momentum and add it to a new column in df;
## Momentum is defined as close [today] / close [5 days ago]
df['Momentum'] = df['Close'] / df['Close'].shift(short_window)

## calculate the standard deviation of SMA over a rolling window
## ddof means degree of freedom, set it to zero to get the population std
df['STD'] =df['Close'].rolling(short_window).std(ddof=0)

## calculate the Bollinger Band for each day
## BB > 1 means the closing price is above the upper band
## BB < -1 means the closing price is below the lower band
df['BB'] = (df['Close'] - df['SMA']) / (2 * df['STD'])

## calculate William's %R for each day

## calculate Rate of Change (ROC) for each day


## calculate the percent change of closing price for each day
## shift(1) means yesterday (applies to each element of df)
increase = df['Close'] - df['Close'].shift(1)
df['Percent_Change'] = (increase / df['Close'].shift(1))*100

## shift percent change to the previous day so that it now represents the 
## percent change for the next day (shift df elements up by 1 using -1)
df['Percent_Change'] = df['Percent_Change'].shift(-1)


#%% ANN TRAINING

## start training ANN using the df file contains historical data and 
## information that was just populated above
print('\n\n********* NOW START TRAINING ANN USING', historical_data_file,'*********')
time.sleep(3)

## remove rows with invalid inputs (i.e., nan) and 
## create input and output arrays for ANN
## starting from day 25 to te end, but excluding the end (due to -1)
## we will predict the precent change of the last day recorded in csv (today) 
X = np.array(df[long_window:-1][['SMA', 'EMA', 'Momentum', 'BB']])
Y = np.array(df[long_window:-1]['Percent_Change'])

## create a model for the ANN
model = keras.Sequential()

# Create ANN with 6 inputs + 2 hidden layers + 1 output layer
## first hidden layer that accepts 6 input features
## the hidden layer will have 4 neurons;
## dense means every neuron in the layer connects to every neuron in the
## previous layer;

## add another hidden layer with 3 neurons to the ANN

## add an output layer with a single output (percent change)


## set the optimization algorithm used for minimizing loss function
## use gradient descent (adam) to minimize error (loss)

## train the ANN model using 200 iterations


## training with more iterations will yield better results 
## build different ANN configurations for better results
## use different activation functions for better results
## use different optimizers adam or SGD (stochastic gradient descent)
## model.fit(X, Y, epochs=2000)

print_weights(weights)
print('\n\n********** ANN training complete **********\n\n')

#%% ANN PREDICTION

## insert the inputs for the latest trading day into an array
latest_SMA = df.iloc[-1]['SMA']
latest_EMA = df.iloc[-1]['EMA']
latest_Momentum = df.iloc[-1]['Momentum']
latest_BB = df.iloc[-1]['BB']
latest_inputs = np.array([[latest_SMA, latest_EMA, latest_Momentum, latest_BB]])

prediction = model.predict(latest_inputs)[0,0]



print('\n***************************************')
print('ANN Predicted Next Day Stock Movement: %+.2f%%' % (prediction))
print('***************************************')


