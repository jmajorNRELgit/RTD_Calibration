# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 07:57:58 2019

@author: jmajor
"""

import pandas as pd
import matplotlib.pyplot as plt

file = 'C:/Users/jmajor/Desktop/github/RTD_Calibration/New calibration programs/data/Mar 12 2019, 09_33_51.csv'

df = pd.read_csv(file)

RTD2, RTD3, RTD4, RTD5, RTD6, RTD7, RTD8 = [],[],[],[],[],[],[]

REF_temp = list(df['REF_temp'])
time = list(df['Time'])

for i in range(len(df)):
    data = list(map(float,df['RTD temps'][i].lstrip('[').rstrip(']').split(',')))
    RTD2.append(data[0])
    RTD3.append(data[1])
    RTD4.append(data[2])
    RTD5.append(data[3])
    RTD6.append(data[4])
    RTD7.append(data[5])
    RTD8.append(data[6])


data_dictionary = {'Time': time, 'REF_temp':REF_temp, 'RTD2':RTD2, 'RTD3':RTD3,'RTD4':RTD4,'RTD5':RTD5,'RTD6':RTD6,'RTD7':RTD7, 'RTD8':RTD8}

df2 = pd.DataFrame(data_dictionary)

#rearrange columns
cols = df2.columns.tolist()
df2 = df2[cols[-1:] + cols[:-1] ]

df2.to_csv('RTD calibration data_rearranged.csv', index = False)
