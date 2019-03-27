# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 08:46:56 2019

@author: jmajor
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np

'''Data selection'''
#########################################################################################################################################

#file = 'C:/Users/jmajor/Desktop/github/RTD_Calibration/New calibration programs/data/RTD calibration data_rearranged.csv'

file = 'C:/Users/jmajor/Desktop/github/RTD_Calibration/New calibration programs/data/old cal cata_rearranged.csv'

df = pd.read_csv(file)

#time = df['Time']
#REF_temp = df['REF_temp']
#RTD2, RTD3, RTD4, RTD5, RTD6, RTD7, RTD8 = df['RTD2'], df['RTD3'], df['RTD4'], df['RTD5'], df['RTD6'], df['RTD7'], df['RTD8']

REF_temp = df['REF']
RTD2, RTD3, RTD4, RTD5, RTD6, RTD7, RTD8 = df['2'], df['3'], df['4'], df['5'], df['6'], df['7'], df['8']

RTD_data_list = [RTD2, RTD3, RTD4, RTD5, RTD6, RTD7, RTD8]

x = range(len(RTD2))


fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(111)

ax1.plot(x,RTD2, label = 'RTD2')
ax1.plot(x,RTD3, label = 'RTD3')
ax1.plot(x,RTD4, label = 'RTD4')
ax1.plot(x,RTD5, label = 'RTD5')
ax1.plot(x,RTD6, label = 'RTD6')
ax1.plot(x,RTD7, label = 'RTD7')
ax1.plot(x,RTD8, label = 'RTD8')
ax1.plot(x, REF_temp, label = 'REF temp')
ax1.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
fig.tight_layout()



calibration_data = []
def onselect(xmin, xmax):
    indmin, indmax = np.searchsorted(x, (xmin, xmax))
    indmax = min(len(x) - 1, indmax)
    #print('X min and max: ',indmin, indmax)

    calibration_data.append([np.average(RTD2[indmin:indmax]),
                             np.average(RTD3[indmin:indmax]),
                             np.average(RTD4[indmin:indmax]),
                             np.average(RTD5[indmin:indmax]),
                             np.average(RTD6[indmin:indmax]),
                             np.average(RTD7[indmin:indmax]),
                             np.average(RTD8[indmin:indmax]),
                             np.average(REF_temp[indmin:indmax])])



# Set useblit=True on most backends for enhanced performance.
span = SpanSelector(ax1, onselect, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='red'))

plt.show(block = True)
#########################################################################################################################################



'''Calibration'''
#########################################################################################################################################
RTD2_data_points = [i[0] for i in calibration_data]
RTD3_data_points = [i[1] for i in calibration_data]
RTD4_data_points = [i[2] for i in calibration_data]
RTD5_data_points = [i[3] for i in calibration_data]
RTD6_data_points = [i[4] for i in calibration_data]
RTD7_data_points = [i[5] for i in calibration_data]
RTD8_data_points = [i[6] for i in calibration_data]
REF_temp_data_points = [i[7] for i in calibration_data]

RTD_list = [RTD2_data_points, RTD3_data_points, RTD4_data_points, RTD5_data_points, RTD6_data_points, RTD7_data_points, RTD8_data_points]
RTD_coefficients = []

fitted_RTD_data = []

'''finding coeffiecients'''
for i in range(len(RTD_list)):
    cof = np.polyfit(RTD_list[i], REF_temp_data_points, 3)
    RTD_coefficients.append(cof)
    fit = np.poly1d(cof)

    fitted_RTD_data.append(list(map(fit, RTD_data_list[i] )))



for i in RTD_coefficients:
    print(i)



for i in range(len(fitted_RTD_data)):
    plt.plot(x,fitted_RTD_data[i], label = 'RTD {}'.format(i+2))



plt.plot(x,REF_temp, label = 'REF')

#plt.plot(x,RTD2, label = 'RTD2')
#plt.plot(x,RTD3, label = 'RTD3')
#plt.plot(x,RTD4, label = 'RTD4')
#plt.plot(x,RTD5, label = 'RTD5')
#plt.plot(x,RTD6, label = 'RTD6')
#plt.plot(x,RTD7, label = 'RTD7')
#plt.plot(x,RTD8, label = 'RTD8')
plt.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
plt.tight_layout()

cal_dict = {'Channel 1:' : RTD_coefficients[0], 'Channel 2:' : RTD_coefficients[0], 'Channel 3:' : RTD_coefficients[1], 'Channel 4:' : RTD_coefficients[2], 'Channel 5:' : RTD_coefficients[3], 'Channel 6:' : RTD_coefficients[4], 'Channel 7:' : RTD_coefficients[5], 'Channel 8:' : RTD_coefficients[6],}

k = pd.DataFrame(cal_dict)

#k.to_csv(r'C:\Users\jmajor\Desktop\github\RTD_Calibration\New calibration programs\data\110_to_210C_coefficients.csv')

#from plotly.offline import plot
#
#import plotly.graph_objs as go
#
#
#data_to_graph = []
#
#k = 2
#for i in fitted_RTD_data:
#    # Create a trace
#    trace = go.Scatter(
#        y = i,
#        name = 'RTD{} fitted'.format(k)
#    )
#    data_to_graph.append(trace)
#    k+=1
#
#REF = go.Scatter(
#        y = REF_temp,
#        name = 'REF temp'
#    )
#data_to_graph.append(REF)
#
#data = data_to_graph
#
#plot(data)