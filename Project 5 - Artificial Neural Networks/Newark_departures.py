#-------------------------------- EE 6530 ---------------------------------
#| Project #5A -  Flight Planning using ANN                               |
#--------------------------------------------------------------------------
#
# Instructor            : Prof. Uyar
#
# Student 1 Name        : Sanjidah Wahid
# Student 1 CCNY email  : swahid000
# Student 1 Log In Name : ee59837_16
# Student 2 Name        : 
# Student 2 CCNY email  :
# Student 2 Log In Name : 
# Student 3 Name        :
# Student 2 CCNY email  :
# Student 3 Log In Name :
# --------------------------------------------------------------------------
# | I UNDERSTAND THAT COPYING PROGRAMS FROM OTHERS WILL BE DEALT           |
# | WITH DISCIPLINARY RULES OF CCNY.                                       |
# --------------------------------------------------------------------------

import numpy as np
import pandas as pd
import time
from datetime import datetime
from tensorflow import keras

# import print_weights as pw
# call: pw.print_weights()

def print_weights(weights):
    # weights = model.get_weights();
    print('\n******* WEIGHTS OF ANN *******\n') 
    for i in range(int(len(weights)/2)):
        print('Weights W%d:\n' %(i), weights[i*2])
        print('Bias b%d:\n' %(i), weights[(i*2)+1])
#END print_weights()

#%% ANN TRAINING
print('\n')
print('**************************************************************************************')     
print('****  THANK YOU FOR USING THE NEWARK LIBERTY INTERNATIONAL AIRPORT NETWORKING ANN ****')
print('**************************************************************************************')

# prompt user to train or load an ANN model
option_list = ['1','2']
option = ''
while option not in option_list:  
    print('\nOPTIONS:')
    print('1 - Train a new ANN model')
    print('2 - Load an existing model')
    
    option = input('\nSelect an option by entering a number: \n')
    if option not in option_list:
        message = 'Invalid input: Input must be one of the following - '
        print(message, option_list)
        time.sleep(2)
        
if option == '1':
    ## OPTION 1: TRAIN A NEW ANN MODEL
    Newark_Airport_check = 'Newark_Airport_check.csv'
    
    print('\n********* NOW TRAINING ANN USING', Newark_Airport_check,'*********')
    time.sleep(3)
    
    ## load the training data
    df = pd.read_csv(Newark_Airport_check)
    
    ## the training data contains 7 columns:
    ##
    ##      timestamp - the date and time the sample was recorded
    ##      departures - the number of planes that departed over the last hour
    ##      num_passengers - the number of passengers over the last hour
    ##      is_weekend - boolean that is 1 (true) if the day is a weekend
    ##      temp_c - the temperature in Celcius
    ##      wind_speed - wind speed in km/h
    ##      weather_code - category of weather: 3 = clear
    ##                                          4 = few clouds
    ##                                          5 = cloudy
    ##                                          6 = fog
    ##                                          7 = rain
    ##                                          8 = thunderstorm
    
    ## the timestamp column of df are stored as strings. We want to
    ## convert each timestamp string into a datetime objects using the 
    ## function datetime.strptime(). The first input of datetime.strptime() 
    ## is the string you want to convert, and the second input is the 
    ## format of the string, where
    ## %m = month, %d = day, %Y = year, %H = hour, %M = minute.
    ##
    ## create lambda function to perform conversion and return the hour.
    getHour = lambda timestamp: datetime.strptime(timestamp, '%m/%d/%Y %H:%M').hour    ## apply the lambda function to every timestamp in column df['timestamp']

    ## apply the lambda function to every timestamp in column df['timestamp']
    df['hour']= df['timestamp'].apply(getHour)

    ## define input matrix X (get rid of columns called timestamp and
    ## num_passengers)
    X = np.array(df.drop(['timestamp', 'num_passengers'], axis=1))

    ## define expected output matrix Y (column num_passengers)
    Y = np.array(df['num_passengers'])
    
    ## create a model for the ANN
    model = keras.Sequential()

    ## add a hidden layer that accepts 6 input features (time_hour,
    ## departures, temperature_f, wind_speed, is_weekend, weather_code)
    ## Dense means every neuron in the layer connects to every neuron in the
    ## previous layer.
    model.add(keras.layers.Dense(6, activation='relu', input_shape=(6,)))

    ## add additional hidden layer(s) (if needed) to the ANN
    model.add(keras.layers.Dense(3, activation='relu'))
    model.add(keras.layers.Dense(3, activation='relu'))

    ## add an output layer with a single output 
    model.add(keras.layers.Dense(1, activation='linear'))
    
    ## set the optimization algorithm used for minimizing loss function
    ## use gradient descent (adam) to minimize error (loss)
    model.compile(optimizer='adam', loss='mean_squared_error')

    ## train the ANN model using 1000 iterations
    model.fit(X, Y, epochs=1000)

    
    print('\n\n********** ANN training complete **********\n\n')    
elif option == '2':
    ## OPTION 2: LOAD ANN MODEL FROM FILE
    
    message = 'Enter the file name of the ANN Model you want to load: \n'
    load_file = input(message)
    #load_file = input('It must be a .h5 file')
    
    ## if file name does not end with '.h5', add '.h5' to the file name
    if load_file[-3:] != '.h5':
        load_file += '.h5'
    ## load the ANN model from load_file
    model = keras.models.load_model(load_file)
    
    print('\n\n****** SUCCESSFULLY LOADED ANN MODEL FROM', load_file,'******')   
else:
    print('ERROR: INVALID OPTION SELECTED')
    ## raise an exception to terminate the program
    raise ValueError()

weights = model.get_weights();
print_weights(weights)

#%% BIKE SHARING PREDICTION USING ANN
input('\n\n********** Press ENTER to start using the ANN **********\n\n')
finished = False
while not finished:
    ## prompt user for inputs
    departures = float(input('\n\nEnter the total number of plane departures in the past hour: \n'))
    hour = float(input('Enter hour of the day (military): (0-23) \n'))
    is_weekend = input('Is it the weekend? (y/n): \n')
    if is_weekend == 'y':
        is_weekend = 2
    else:
        is_weekend = 1
    temperature_f = float(input('Enter the outdoor temperature in fahrenheit: \n'))
    weather_code = int(input('Enter weather code: (3 = clear, '
                        + '4 = partly cloudy, 5 = cloudy, '
                        + '7 = freezing rain, 8 = snow) \n'))
    wind_speed = float(input('Enter wind speed: (mph) \n'))
    user_input = np.array([[departures, temperature_f, wind_speed, is_weekend, weather_code, hour]])
    prediction = model.predict(user_input)
    
    ## restrict prediction to non-negative values
    if prediction < 0:
        prediction = 0;
    else:
        pass

    ## display prediction
    print('\n*****************************************')
    print('ANN Predicted number of passengers departing from Newark Liberty International Airport: ', int (prediction))
    print('*****************************************')
    ## ask user if they would like to continue
    choice = ''
    while choice not in ['y','n']:
        choice = input('\n\nWould you like to continue? (y/n): \n')
        if choice == 'y':
            pass
        elif choice == 'n':
            finished = True
        else:
            print("Invalid input: Input must be 'y' or 'n'")
    #END WHILE
#END WHILE

## ask user if they would like to save the ANN model
choice = ''
while choice not in ['y','n']:
    choice = input('\n\nWould you like to save the ANN model? (y/n): \n')
    if choice == 'y':
        save_name = input('\n\nEnter a name for the save file: \n')
        ## if file name does not end with '.h5', add '.h5' to the file name
        if save_name[-3:] != '.h5':
            save_name += '.h5'
        model.save(save_name)
        print('\n\n')
        print('***** ANN MODEL SUCCESSFULLY SAVED AS '+save_name+' *****')
    elif choice == 'n':
        pass
    else:
        print("Invalid input: Input must be 'y' or 'n'")
#END WHILE

