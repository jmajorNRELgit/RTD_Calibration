import NI_RTD_DAQ_CLASS
import BATH_class
import REF_class
from time import sleep
import csv
import numpy as np

'''change the port names here!! (run ports.py to see what ports are being used)'''
#####################################################
bath_port = 'COM4'
bath = BATH_class.bath()
bath_com = bath.establish_bath_com(bath_port)

REF_port = 'COM9'
REF = REF_class.REF()
REF_com = REF.establish_REF_com(REF_port)

#DAQ_port = '/dev/ttyUSB1'
DAQ = NI_RTD_DAQ_CLASS.DAQ()
#####################################################


def ongoing_REF_measurements(minutes):
    ongoing_ref_temp = []
    time_interval = minutes*60/20 #*60 to get number of seconds, /20 because there is a sleep(20) function for a delay
    
    for i in range(int(time_interval)):
        ongoing_ref_temp.append(REF.measure_REF_temp())
        print(ongoing_ref_temp[-1:], ': {0}, std = {1}'.format(len(ongoing_ref_temp), np.std(ongoing_ref_temp[-100:])))
        with open('ongoing_REF_temp.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(ongoing_ref_temp[-1:])
        sleep(20)
    return ongoing_ref_temp

def take_calibration_measurement(bath_set_point):
    DAQ_temp_list = [] 
    REF_temp_list = []
    
    '''fix this'''
    RTD_locations = [1,2,3,4,5,6,7,8]
    
    for i in range(20):
        print('\nMeasuring temperature {0}'.format(str(i)))
        REF_temp_list.append(REF.measure_REF_temp())
        DAQ_temp_list.append(DAQ.read_DAQ_temp())
        sleep(1)
        
    #Combines the raw temperature lists into one list and saves to a CSV file
    combine_temp_list = []
    for i in range(len(REF_temp_list)):
        combine_temp_list.append(DAQ_temp_list[i] + [REF_temp_list[i]])

    with open('Calibration at {0} degrees.csv'.format(bath_set_point), 'a') as f:
        writer = csv.writer(f)
        writer.writerow(RTD_locations + ['REF'])
        for i in combine_temp_list:
            writer.writerow(i)
    sleep(5)

def main_program( bath_set_point, bath_end_temp, incriment):
    
    
    
    while True:
        #set bath temperature (because of overshoot, it sets the bath below by 2 degrees, sleeps 5 minutes, then sets to the actual set point)
        bath.set_bath_setpoint(bath_set_point-2)
        print('Bath temperature set to {0}'.format(bath_set_point-2))
        sleep(60*10)
        bath.set_bath_setpoint(bath_set_point)
        print('Bath temperature set to {0}'.format(bath_set_point))
        #wait 120 minutes while saving the REF temp to a csv file and printing the temp and standard deviation info
        ongoing_ref_temp = ongoing_REF_measurements(60)
            
        #check if the temp is within range and the standard deviation is less than .005
        while True:
            if (ongoing_ref_temp[-1] >= bath_set_point - 1 and ongoing_ref_temp[-1] <= bath_set_point + 1) and np.std(ongoing_ref_temp[-100:]) < .005:
                #takes measurements for calibration
                take_calibration_measurement(bath_set_point)
                break
            else:
                #waits for 10 minutes while still recording the REF temp
                print('Waiting 10 minutes')
                ongoing_ref_temp = ongoing_REF_measurements(10)
                
        
        #if the bath has reached the end temp, set bath to 30 degrees and break
        if bath_set_point >= bath_end_temp:
             print('Calibration finished, bath set to 30 degrees')
             bath.set_bath_setpoint(30)
             break
        else:
            bath_set_point += incriment

if __name__ == '__main__':
    bath_set_point = float(input('Please enter the bath starting temp: ')) or 120
    bath_end_temp = float(input('\nPlease enter the bath end temp: ')) or 220
    incriment = float(input('\nPlease enter the temperature incriment: ')) or 10
    
    main_program(bath_set_point, bath_end_temp, incriment)