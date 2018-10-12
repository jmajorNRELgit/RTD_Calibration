# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 12:12:10 2018

@author: jmajor
"""

import pandas as pd
import numpy as np
import glob
np.set_printoptions(suppress=True) #prevents numpy from printing in scientific notation


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
        self.cofficient = None
        
    def set_cof(self,cof):
        self.cofficient = cof
        
    def poly_fit(self):
        fit = np.poly1d(self.cofficient)
        return fit(self.channel_data)
        
    
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
        
for i in range(8):
    cof = np.polyfit(channel_data[i].channel_data, channel_data[8].channel_data, 3)
    channel_data[i].set_cof(cof)
    
for i in range(8):
    print(np.round((channel_data[i].poly_fit() - channel_data[8].channel_data),6))
    