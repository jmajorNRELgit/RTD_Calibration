# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 12:12:10 2018

@author: jmajor
"""
import csv
import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
np.set_printoptions(suppress=False) #prevents numpy from printing in scientific notation

#class to hold the raw data
class raw_data():
    
    def __init__(self, temperature, data):
        self.temp = temperature
        self.data = data
        self.mean_data = self.data.mean()
        self.std_data = np.std(self.data)

#class to hold the channel specific data through the whole temperature range 
class channel_data_class():
    
    def __init__(self, channel_data,name):
        self.channel_name = name
        self.channel_data = channel_data
        self.coefficient = None
        
    def set_cof(self,cof):
        self.coefficient = cof
        
    def poly_fit(self):
        fit = np.poly1d(self.coefficient)
        return fit(self.channel_data)
        
    
#glob grabs all the filenames and column_names is used in the pandas dataframe
files = glob.glob(r'C:\Users\jmajor\Desktop\github\RTD_Calibration\Raw temp data\*.csv')
column_names = ['Channel 1','Channel 2','Channel 3','Channel 4','Channel 5','Channel 6','Channel 7','Channel 8','REF',]



temps = ['50','60','70', '80', '90', '100', '120', '130','140','150','160','170','180','190','200','210'] #this is the temperatures used in the raw_data class

obj = [] #this will be a list of raw_data object instances
i = 0
for file in files: #reads the raw data into the raw_data class
    obj.append(raw_data(file[-17:-12], pd.read_csv(file, names = column_names, skiprows = 1)))
    i+=1


channel_data = []  #this will be a list of channel_data object instances
for i in range(9): #range 9 because 8 daq channels and one ref channel
    lis = [] #list to hold the channel temp data. resets 9 times. onece for each channel
    for o in obj:
        lis.append(o.mean_data[i]) #the mean of the 20 samples taken
    channel_data.append(channel_data_class(lis,column_names[i]))

#uses np.polyfit to fit the daq data to the ref data. Saves info in the channel_data class
for i in range(8):
    cof = np.polyfit(channel_data[i].channel_data, channel_data[8].channel_data, 5)
    channel_data[i].set_cof(cof)

#prints the difference between the fit channel temperatures and the ref temps
for i in range(8):
    print(channel_data[i].channel_name,(channel_data[i].poly_fit() - channel_data[8].channel_data))
    plt.plot(np.round((channel_data[i].poly_fit() - channel_data[8].channel_data),6), label = channel_data[i].channel_name )
    plt.legend()
  
#Print the coefficients to a csv file
cof_list = pd.DataFrame()
for i in range(8):
    cof_list['Channel {}:'.format(i+1)] = pd.Series(channel_data[i].coefficient)
cof_list.to_csv('coefficient_list.csv')
    
    