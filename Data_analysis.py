# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 12:12:10 2018

@author: jmajor
"""

import pandas as pd
import numpy as np
import glob

#read file and give column names

#df = pd.read_csv('C:/Users/jmajor/Desktop/Calibration raw data/Calibration at 50.0 degrees.csv', names = column_names, skiprows = 1)
#
##print out the standard deviation of each column to three decimal places
#for i in range(9):
#    print(df.columns[i], 'STD: ',np.around(np.std(df.iloc[:,i]),4),)
#print('\n')
#    
#    
##print out the mean of each column
#print('Channel mean:')
#print(df.mean(0))
#
#class to hold the raw calibration data
class raw_data():
    
    def __init__(self, temperature, data):
        self.temp = temperature
        self.data = data
        self.mean_data = self.data.mean()
        self.std_data = np.std(self.data)
        
class channel_data_class():
    
    def __init__(self, channel_data,name):
        self.channel_name = name
        self.channel_data = channel_data
        
    
#glob grabs all the filenames and column_names is used in the pandas dataframe
files = glob.glob(r'C:\Users\jmajor\Desktop\github\RTD_Calibration\Raw temp data\*.csv')
column_names = ['Channel 1','Channel 2','Channel 3','Channel 4','Channel 5','Channel 6','Channel 7','Channel 8','REF',]


obj = [] #this will be a list of raw_data object instances
temps = ['50','60','70', '80', '90']

i = 0
for file in files:
    
    obj.append(raw_data(temps[i], pd.read_csv(file, names = column_names, skiprows = 1)))
    i+=1

channel_data = []
for i in range(9):
    lis = []
    for o in obj:
        lis.append(o.mean_data[i])
    channel_data.append(channel_data_class(lis,column_names[i]))
        
    