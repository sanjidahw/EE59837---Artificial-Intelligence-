#-------------------------------- EE 59837 --------------------------------
#| Project #7 -  Natural language processing using ANN                    |
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

# Using tweets from the CDC, predict the movement of Delta Airline stocks. 
# The tweets range from June 2020 - Aug 2020.  
# The days where no data was present are given in arrays called missing_days 
# and invalid days.

import datetime
from datetime import date
import math
import numpy as np
import pandas as pd
from tensorflow import keras
import re

#%% Function to remove punctuation and web links from tweets
# @\S+|https?://\S+ - matches either a substring which starts with @
# and contains non-whitespace characters \S+ OR a link(url) which
# starts with http(s)://
def clean_tweet(tweet):
    return ' '.join(re.sub('(@[A-Za-z0-9]+) | ([^0-9A-Za-z \t]) | (\w+:\/\/\S+)',
                ' ', tweet).split())

def str_to_date(string):
    return datetime.datetime.strptime(string, '%Y-%m-%d').date()

def print_weights(weights):
    # weights = model.get_weights();
    print('\n******* WEIGHTS OF ANN *******\n')
    for i in range(int(len(weights)/2)):
        print('Weights W%d:\n' %(i), weights[i*2])
        print('Bias b%d:\n' %(i), weights[(i*2)+1])

def normalize_column(dataframe, col_name):
    maximum = max(dataframe[col_name])
    minimum = min(dataframe[col_name])
    dataframe[col_name] = (dataframe[col_name] - minimum)/(maximum-minimum)
    return dataframe[col_name]

#%% Load in file, remove punctuation and weblinks from all tweets and then
#   perform sentiment analysis.
print('\n\n********** CLEANING TWEETS **********\n\n')
filename = "CDC_travel_Health.csv"
df = pd.read_csv(filename)
df["Clean Tweet"] = df['text'].apply(lambda x: clean_tweet(x))
df['created_at'] = pd.to_datetime(df['created_at']).dt.date

#%% Data cleaning and processing
# Check if the tweet contains any keywords - remove all tweets that don't
print('\n\n********** IDENTIFYING KEY WORDS **********\n\n')

# Define the key words here (as a list):
key_words = ['travel','increase', 'distancing', 'contact',  'COVID', 'mask','pandemic', 'home', 'gathering', 'limit', 'spread', 'restrictions','stay', 'chance', 'international']

df['noof_keywords'] = np.where(df['text'].str.contains('|'.join(key_words)),0,0)

for key_word in key_words:
    #df[key_word] = np.where(df.text.str.contains(key_word), 1, 0)
    df[key_word] = np.where(df["Clean Tweet"].str.contains(key_word), 1, 0)


invalid_days = ['2020-07-03','2020-07-04','2020-07-24','2020-07-25','2020-07-26','2020-08-16','2020-08-18','2020-08-19']
noof_invalid_days = len(invalid_days)
invalid_days = list(map(lambda x:str_to_date(x),invalid_days))


############## Moving Days From Invalid and From Weekends ##############
for day in df['created_at']:
    new_day = day
    while new_day in invalid_days or new_day.weekday() >= 5:
        new_day += datetime.timedelta(days = 1)
    df.loc[df['created_at'] == day, 'created_at'] = new_day
########################################################################

# results = Counter()
# df['Clean Tweet'].str.lower().str.split().apply(results.update)
# print(results)
# df["Clean Tweet"] = df['text'].apply(lambda x: clean_tweet(x))

############## Adding Same Date Tweets Together ##############

for key_word in key_words:
    df['noof_keywords'] += df[key_word]

grouped_df = df.drop(columns = ['text',"Clean Tweet"])
grouped_df = grouped_df.groupby(by = 'created_at').sum().reset_index()

#%% Stock prices
filename = "Delta_Airlines_Stock.csv"
delta_df = pd.read_csv(filename)

delta_df['percent change'] = delta_df['Close'].pct_change()
delta_df['Date'] = pd.to_datetime(delta_df['Date']).dt.date

for index, row in delta_df.iterrows():
    if row['Date'] in invalid_days:
        delta_df = delta_df.drop(index)
delta_df = delta_df.reset_index(drop = True)

#### Input Data ######

grouped_df['day_opening'] = delta_df['Open']
grouped_df['units_traded'] = delta_df['Volume']


grouped_df['day_opening'] = normalize_column(grouped_df,'day_opening')
grouped_df['units_traded'] = normalize_column(grouped_df,'units_traded')

features = ['noof_keywords','day_opening','units_traded'] + key_words

############## ANN Setup ##############
days_to_predict = 10 + noof_invalid_days
x = np.array(grouped_df.loc[1:len(grouped_df),features])
y = np.array(delta_df.loc[1:len(grouped_df),'percent change'])

val_x = np.array(grouped_df.loc[len(grouped_df) - days_to_predict + 1: ,features])
val_y = np.array(delta_df.loc[len(grouped_df) - days_to_predict + 1:,'percent change'])

model = keras.Sequential()
model.add(keras.layers.Dense(1024, activation = 'relu', input_shape = (len(features),)))
model.add(keras.layers.Dense(512, activation = 'relu'))
model.add(keras.layers.Dense(256, activation = 'relu'))
model.add(keras.layers.Dense(128, activation = 'relu'))
model.add(keras.layers.Dense(1, activation = 'linear'))

model.compile(optimizer='adam',
                    loss='mean_absolute_error',
                    metrics = ['mean_absolute_error'])

model.fit(x, y, epochs = 1200, validation_data = (val_x, val_y))
##############################################################
# weights = model.get_weights()
# print_weights(weights)
print('\n\n********** ANN training complete **********\n\n')

# %%  make predictions
noof_correct_movement = 0
noof_predictions = 0
diffs = []
input_features = []
print('\n\n********** ANN PREDICTIONS **********\n\n')
for i in range(int(days_to_predict), noof_invalid_days,-1):
    input_features.clear()
    noof_predictions += 1
    actual_change = delta_df.iloc[(-1*i)+1]['percent change']
    for feature in features:
        input_features.append(grouped_df.iloc[-1*i][feature])
    predicted_change = model.predict(np.array([input_features]))[0,0]

    print(f"The predicted change for {grouped_df.iloc[(-1*i)+1]['created_at']}",
          end='')
    print(f" was: {predicted_change:.5f}")
    print(f"Actual change was for {delta_df.iloc[(-1*i)+1]['Date']} was: ",
          end='')
    print(f"{round(actual_change,4)}\n")

    if (predicted_change * actual_change) > 0:
        diffs.append(math.fabs(predicted_change - actual_change))
        noof_correct_movement += 1

percent_correct = (noof_correct_movement/noof_predictions) * 100
print(f"ANN was correct in predicting the movement ", end = '')
print(f"{((noof_correct_movement/noof_predictions) * 100):.2f}% of the time in",
      end='')
print(f" {noof_predictions} predictions.")
average_diff = round(sum(diffs)/len(diffs),5)
print(f"The average error of the correct predictions were", end='')
print(f" {average_diff* 100.0:.1f} %")

with open('output.txt','a') as output_file:
    output_file.write(f'{date.today()} percentage of times correct prediction:')
    output_file.write(f' {round(percent_correct,1)} % ')
    output_file.write(f' with error {average_diff* 100.0:.1f}%\n')
