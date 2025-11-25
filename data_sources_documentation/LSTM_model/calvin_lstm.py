#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 14:09:23 2025

@author: msdogan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings('ignore') # Suppress all warnings

# convert time series into supervised learning problem
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = pd.DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

# transform series into train and test sets for supervised learning
def prepare_data(series, n_test, n_lag, n_seq):
    # extract raw values
    raw_values = series#.values
    raw_values = raw_values.reshape(len(raw_values), 1)
    # transform into supervised learning problem X, y
    supervised = series_to_supervised(raw_values, n_lag, n_seq)
    supervised_values = supervised.values
    # split into train and test sets
    train, test = supervised_values[0:-n_test], supervised_values[-n_test:]
    return train, test

# fix random seed for reproducibility
tf.random.set_seed(7)

# read data
df = pd.read_csv('gw_inflows_kaf_1921-1993_sc_2.csv', header=0, parse_dates=[0], index_col=0)
df = df.set_index(pd.DatetimeIndex(df.index))

# configure
n_lag = 1
n_seq = 24
test_portion = 0.33
length = len(df)
n_test = int(length*test_portion)

# time range for data to be estimated
f_range = pd.date_range(start ='1993-10-31', end ='2015-09-30', freq ='M')

prediction = pd.DataFrame()
for key in df.keys():
    dataframe = df[key]
    dataset = np.array(dataframe.values)
    dataset = np.reshape(dataset,(-1,1))
    
    # normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    
    # for every time-step (month) predict data and append to estimate next month's data
    futureY = []
    for val in f_range:
        print('****************')
        print(f'subbasin: {key}, time step: {val}')
        print('****************')
        # prepare data
        train, test = prepare_data(dataset, n_test, n_lag, n_seq)
        data = np.concatenate((train,test))
        
        col_names = []
        for n in range(0,n_seq+1):
            col_names.append(f't-{n_seq-n}')
        
        data = pd.DataFrame(data,columns=col_names)
        # data.to_csv('organized_data.csv')
        
        if val==f_range[0]:
            # calculate correlations between real-valued attributes
            corMat = data.corr()
            fig, ax = plt.subplots(figsize=(8, 6))
            # visualize correlations using heatmap
            sns.heatmap(corMat, vmin=-1, vmax=1, cmap='YlGnBu', linewidths=.5,
                        cbar_kws={'label': 'correlation', 'ticks': [-1, 0, 1]}, ax=ax)
            plt.yticks(rotation='horizontal', fontsize=9)
            plt.xticks(rotation='vertical', fontsize=9)
            plt.title("Cross-Correlation of Attribute Values",
                      loc='center', fontweight='bold')
            plt.tight_layout()
            # plt.subplots_adjust(left=0.25, right=0.99, top=0.95, bottom=0.4)
            plt.savefig('corrmap_'+key+'.png', transparent=False, dpi=300)
            plt.close(fig)
            # plt.show()
        
        # last column is label (t), other columns are input features
        X = np.array(data.iloc[:, :-1].values)
        Y = np.array(data.iloc[:, -1].values)
        
        # split with specified train and test set
        # trainX, testX = X[0:len(train),:], X[len(train):,:]
        # trainY, testY = Y[0:len(train)], Y[len(train):]
        
        # split randomly
        trainX, testX, trainY, testY = train_test_split(X, Y, test_size=test_portion, random_state=42)
        
        # reshape input to be [samples, time steps, features]
        trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
        testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
        
        # create the LSTM network
        model = Sequential()
        model.add(LSTM(200, input_shape=(trainX.shape[1], trainX.shape[2])))
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='linear'))
        model.compile(loss = 'MeanSquaredError', metrics=['MAE'], optimizer='Adam')
        # model.summary()
        
        # fit training data
        model.fit(trainX, trainY, epochs=30, batch_size=1, verbose=2)
        
        # make predictions
        trainPredict = model.predict(trainX)
        testPredict = model.predict(testX)
        
        # invert predictions
        trainPredict = scaler.inverse_transform(trainPredict)
        trainY = scaler.inverse_transform([trainY])
        testPredict = scaler.inverse_transform(testPredict)
        testY = scaler.inverse_transform([testY])
        
        # calculate performance metrics: root mean squared error and r2
        trainScore = np.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
        print('Train Score: %.2f RMSE' % (trainScore))
        testScore = np.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
        print('Test Score: %.2f RMSE' % (testScore))
        
        r2_train = r2_score(trainY[0], trainPredict[:,0])
        print('Train r2: %.2f r2' % (r2_train))
        r2_test = r2_score(testY[0], testPredict[:,0])
        print('Test r2: %.2f r2' % (r2_test))
        
        # future predictions
        # prepare data
        data_p = dataset[len(dataset)-n_seq:,:]
        trainP, futureP = prepare_data(data_p, len(data_p), 0, 1)
        
        # reshape input to be [samples, time steps, features]
        futureP = np.reshape(futureP, (1, 1, futureP.shape[0]))
        
        # make predictions
        futurePredict = model.predict(futureP)
        futureY.append(scaler.inverse_transform(futurePredict)[0][0])
        
        # append and move to next time-step
        dataset = np.concatenate((dataset,futurePredict))
    prediction[key] = futureY
    
    prediction.index = f_range
    prediction.index.name = 'date'
    prediction.to_csv(key+'_gw_inflow_prediction_1993-2015_sc_2.csv')
