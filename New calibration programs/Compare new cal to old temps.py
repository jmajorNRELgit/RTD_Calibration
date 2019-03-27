# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 14:58:02 2019

@author: jmajor
"""

import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
files = glob.glob(r'C:\Users\jmajor\Desktop\github\RTD_Calibration\Raw temp data\*.csv')

dfs = []

for file in files:
    dfs.append(pd.read_csv(file, index_col = False))

df = pd.concat(dfs).reset_index(drop = True)
df.sort_values(by = '1', inplace = True)
df.reset_index(inplace = True, drop = True)



#
#cols = df.columns.tolist()
#coldf = df[cols[-1:] + cols[:-1] ]

fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(111)




RTD2_coef = [-1.85007372e-07,  2.38760170e-05,  9.71055063e-01,  5.43396077e-02]
RTD3_coef =[-2.14652870e-07,  5.14170069e-05,  9.67894559e-01,  1.80528553e-01]
RTD4_coef =[-3.29183273e-07,  7.69706680e-05,  9.66150562e-01,  8.77098178e-02]
RTD5_coef =[-2.17806531e-07,  4.06967070e-05,  9.68997310e-01,  1.07511404e-01]
RTD6_coef =[ 8.63838984e-08, -8.89703699e-06,  9.71481833e-01,  1.03373532e-01]
RTD7_coef =[-4.34408063e-08, -6.66775681e-06,  9.71735197e-01,  7.01680365e-02]
RTD8_coef =[-2.09064984e-07,  3.84626868e-05,  9.69052962e-01,  8.04150196e-02]

coefs = [RTD2_coef, RTD3_coef,RTD4_coef,RTD5_coef,RTD6_coef,RTD7_coef,RTD8_coef,]

fits = []

for cof in coefs:
    fit = np.poly1d(cof)
    fits.append(fit)


df['2'] = [fits[0](i) for i in df['2']]
df['3'] = [fits[1](i) for i in df['3']]
df['4'] = [fits[2](i) for i in df['4']]
df['5'] = [fits[3](i) for i in df['5']]
df['6'] = [fits[4](i) for i in df['6']]
df['7'] = [fits[5](i) for i in df['7']]
df['8'] = [fits[6](i) for i in df['8']]

ax1.plot(df['REF'], label = 'REF')
ax1.plot(df['2'], label = 'RTD2')
ax1.plot(df['3'], label = 'RTD3')
ax1.plot(df['4'], label = 'RTD4')
ax1.plot(df['5'], label = 'RTD5')
ax1.plot(df['6'], label = 'RTD6')
ax1.plot(df['7'], label = 'RTD7')
ax1.plot(df['8'], label = 'RTD8')
ax1.legend()

