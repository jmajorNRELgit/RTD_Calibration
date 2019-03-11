# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:33:53 2019

@author: jmajor
"""

import NI_RTD_DAQ_CLASS
import BATH_class
import REF_class
from time import sleep
import pandas as pd
import numpy as np
import threading
import time
import numpy as np
import matplotlib.pyplot as plt

'''change the port names here!! (run ports.py to see what ports are being used)'''
#####################################################
bath_port = 'COM13'
bath = BATH_class.bath()
bath_com = bath.establish_bath_com(bath_port)

REF_port = 'COM9'
REF = REF_class.REF()
REF_com = REF.establish_REF_com(REF_port)

DAQ_port = '/dev/ttyUSB1'
DAQ = NI_RTD_DAQ_CLASS.DAQ()
DAQ.set_specific_channels([2,3,4,5,6,7,8])
#####################################################

DAQ_temp_list = []
REF_temp_list = []
elapsed_time = []

start = time.time()

stop = 0

def worker_thread_1():
    while stop == 0:
        DAQ_temp_list.append(DAQ.read_specific_channels())
        REF_temp_list.append(REF.measure_REF_temp())
        elapsed_time.append(time.time() - start)

        if len(DAQ_temp_list) % 50 == 0:
            save_data()



def save_data( path = None):

            if path == None:
                path = 'auto_saved_data'
            else:
                path = path

            DAQ_temp, REF_temp, elapsed_t = syncronize_data()

            data = {'RTD temps': DAQ_temp_list, 'REF_temp': REF_temp, 'Time': elapsed_time}

            df = pd.DataFrame(data)

            file_time = time.strftime("%b %d %Y, %H_%M_%S")
            print('{0}.csv'.format(file_time))

            df.to_csv('{0}/{1}.csv'.format(path,  file_time), index = None)

'''get all the data lists the same length'''
def syncronize_data():
    min_list_length = min([len(DAQ_temp_list), len(REF_temp_list), len(elapsed_time)])

    DAQ_temp = DAQ_temp_list[:min_list_length]
    REF_temp = REF_temp_list[:min_list_length]
    elapsed_t = elapsed_time[:min_list_length]



    return DAQ_temp, REF_temp, elapsed_t


def main_program(bath_set_point, bath_end_temp, incriment):
    global stop

    for i in range(bath_set_point, bath_end_temp, incriment):

        print(i)

        #set bath temperature (because of overshoot, it sets the bath below by 2 degrees, sleeps 10 minutes, then sets to the actual set point)
        bath.set_bath_setpoint(bath_set_point-2)
        print('Bath temperature set to {0}'.format(bath_set_point-2))
        sleep(60*10)
        bath.set_bath_setpoint(bath_set_point)
        print('Bath temperature set to {0}'.format(bath_set_point))
        #time.sleep(60*60*2)
        time.sleep(60*60)


    bath.set_bath_setpoint(30)
    print('Bath set too 30')
    stop = 1



if __name__ == '__main__':
    bath_set_point = int(input('Please enter the bath starting temp: ')) or 120
    bath_end_temp = int(input('\nPlease enter the bath end temp: ')) or 220
    incriment = int(input('\nPlease enter the temperature incriment: ')) or 10

    thread1 = threading.Thread(target=worker_thread_1)
    thread1.start(  )

    main_program(bath_set_point, bath_end_temp, incriment)


