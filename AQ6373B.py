DESCRIPTION = """Optical spectral analyzer program for YOKOGAWA AQ6373B optical spectrum analyzer.

Example
-------
# Preparation
    1. Connect LAN cable between Hub and AQ6373B
    2. AQ6373B System=>Remote Interface (Network VX1-11)
    3. Network Setting=>TCP/IP setting=>Manually set the IP Address/Subnet Mask/Gateway
        ex.) IP address: 192.168.10.100, Subnet Mask: 255.255.252.0, Gateway: 192.168.8.1  
    4. PC, open NI-MAX, Network device, Set TCP/IP settings Hostname (IP address), Device Name (inst0), Address(Ip address)

# Run the data logging program in terminal
    ex.1) 
        python AQ6373B_spectrum_aquisition_v0.3.py -cw 1064 -strw 1024 -stpw 1104 -sen "MID" -res 20 -fib "LARGE" -pts 1001 -lev -20 -sm "SINGLE" -th 3 -int 0

    ex.2) 1061.5-1066.5nm, 3dB, 20pn, 5001points, every 10min
        python AQ6373B_spectrum_aquisition_v0.3.py -cw 1064 -strw 1061.5 -stpw 1066.5 -sen "MID" -res 20 -fib "SMALL" -pts 5001 -lev -20 -sm "SINGLE" -th 3 -int 600

# See help
Resource1: https://github.com/jkrauth/labdevices/blob/main/labdevices/ando.py
Resource2: ¹â¥¹¥Ú¥¯¥È¥é¥à¥¢¥Ê¥é¥¤¥¶¥ê¥â©`¥È¥³¥ó¥È¥í©`¥ë¥æ©`¥¶©`¥º¥Þ¥Ë¥å¥¢¥ë 8.5 ¥µ¥ó¥×¥ë¥×¥í¥°¥é¥à
        
- Author :Kota Koike
- First draft : 2022/9/27
- Update : 2022/11/4

"""

import pyvisa as visa
import serial
from typing import Tuple
from time import sleep
import time
import numpy as np
import sys
import struct
import datetime
import argparse

debug = 0
# =========================================================
# Send a command and check for errors:
# =========================================================
def do_command(command, hide_params=False):
    if hide_params:
        (header, data) = command.split(" ", 1)

        if debug:
            print("\nCmd = '%s'" % header)
        else:
            if debug:
                print("\nCmd = '%s'" % command)

    #print ("\n1")
    Yokogawa.write("%s" % command)

    if hide_params:
      check_instrument_errors(header)
    else:
      check_instrument_errors(command)

# =========================================================
# Send a command and binary values and check for errors:
# =========================================================
def do_command_ieee_block(command, values):
    if debug:
        print("Cmb = '%s'" % command)
    Yokogawa.write_binary_values("%s " % command, values, datatype='B')
    check_instrument_errors(command)

# =========================================================
# Send a query, check for errors, return string:
# =========================================================
def do_query_string(query):
    if debug:
        print("Qys = '%s'" % query)
    result = Yokogawa.query("%s" % query)
    check_instrument_errors(query)
    return result

# =========================================================
# Send a query, check for errors, return binary values:
# =========================================================
def do_query_ieee_block(query):
    if debug:
        print("Qyb = '%s'" % query)
    result = Yokogawa.query_binary_values("%s" % query, datatype='s', container=bytes)
    check_instrument_errors(query, exit_on_error=False)
    return result

# =========================================================
# Check for instrument errors:
# =========================================================
def check_instrument_errors(command, exit_on_error=True):
    while True:
        error_int = int(Yokogawa.query(":SYSTEM:ERROR?"))
        if error_int > 0: # If there is an error string value.
            print("ERROR: %s, command: '%s'" % (error_int, command))
            print("Exited because of error.")
            return

        else: # :SYSTem:ERRor? STRing should always return string.
            #print("ERROR: :SYSTem:ERRor? returned nothing, command: '%s'"% command)
            return

# =========================================================
# Initialize:
# =========================================================
def initialize():
    # Clear status.
    do_command("*CLS")
    # Get and display the device's *IDN? string.
    idn_string = do_query_string("*IDN?")
    print("Identification string: '%s'" % idn_string)
    # Load the default setup.
    #do_command("*RST")

# =========================================================
# Wait:
# =========================================================
def wait():
    """ Wait to send next command until finish current one """
    do_command('*WAI')

# =========================================================
# Set parameters:
# =========================================================
def set_parameters():
    
    do_command(":SENSE:WAVELENGTH:CENTER %sNM" % CENTER_WAVELENGTH)
    qresult = do_query_string(":SENSE:WAVELENGTH:CENTER?")
    print("Center wavelength: %s" % qresult)

    do_command(":SENSE:WAVELENGTH:START %sNM" % START_WAVELENGTH)
    qresult = do_query_string(":SENSE:WAVELENGTH:START?")
    print("Start wavelength: %s" % qresult)

    do_command(":SENSE:WAVELENGTH:STOP %sNM" % STOP_WAVELENGTH)
    qresult = do_query_string(":SENSE:WAVELENGTH:STOP?")
    print("Stop wavelength: %s" % qresult)

    sensitivity_modes = {0: 'NHLD', 1: 'NAUT', 2: 'MID', 3: 'HIGH1', 4: 'HIGH2', 5: 'HIGH3', 6: 'NORMAL',}
    do_command(":SENSE:SENSE %s" % SENSITIVITY)
    qresult = do_query_string(":SENSE:SENSE?")
    #qresult = sensitivity_modes[modes]
    print("Sensitivity: %s" % qresult)

    do_command(":SENSE:BANDWIDTH:RESOLUTION %sPM" % RESOLUTION)
    qresult = do_query_string(":SENSE:BANDWIDTH?")
    print("Resolution: %s" % qresult)

    fiber_type = {0: 'SMALL', 1: 'LARGE',}
    do_command(":SENSE:SETTING:FIBER %s" % FIBER_TYPE)
    qresult = do_query_string(":SENSE:SETTING:FIBER?")
    print("Fiber type: %s" % qresult)

    do_command(":SENSE:SWEEP:POINTS %s" % MEASUREMENT_POINTS)
    qresult = do_query_string(":SENSE:SWEEP:POINTS?")
    print("Measurement points: %s" % qresult)

    do_command(":DISPLAY:TRACE:Y1:RLEVEL %sdbm" % REFERENCE_LEVEL)
    qresult = do_query_string(":DISPLAY:TRACE:Y1:RLEVEL?")
    print("Reference level: %s" % qresult)

    sweep_modes = {1: 'SINGLE', 2: 'REPEAT', 3: 'AUTO', 4: 'SEGMENT',}
    do_command(":INITIATE:SMODE %s" % SWEEP_MODE)
    qresult = do_query_string(":INITIATE:SMODE?")
    print("Sweep mode: %s" % qresult)

# =========================================================
# Do sweep:
# =========================================================
def do_sweep():
    do_command(":INITIATE")

# =========================================================
# Bandwidth Analysis:
# =========================================================
def cal_bandwidth():
    """
    Calculate bandwidth with 3dB threshold
    """
    do_command(":CALCULATE:CATEGORY SWTHRESH") #spectral width analysis, threshold
    do_command(":CALCULATE:PARAMETER:SWTHRESH:TH %s" % THRESHOLD)     
    do_command(":CALCULATE")

# =========================================================
# Save:
# =========================================================
def save(file_name: str):
    wait()
    #Save graphics BMP to external USB
    do_command(f'MMEMORY:STORE:GRAPHICS COLOR,BMP,"{file_name}",EXTERNAL')
    #Save trace CSV to external USB
    do_command(f'MMEMORY:STORE:TRACE TRA,CSV,"{file_name}",EXTERNAL')
    wait()

# =========================================================
# Get x, y data:
# =========================================================
def get_x_data():
    """ Obtain the x axis values in units of nm. """
    #x = do_query_string(":TRACE:X? TRA")
    x = Yokogawa.query(":TRACE:X? TRA")
    #x = x.lstrip().split(',')
    #x = np.array(x, dtype = float)
    return x

def get_y_data():
    """ Obtain the y axis values in the units shown on the screen. """
    #y = do_query_string(":TRACE:Y? TRA")
    y = Yokogawa.query(":TRACE:Y? TRA")
    #y = y.lstrip().split(',')
    #y = np.array(y, dtype = float)
    return y
# =========================================================
# Main program:
# =========================================================
VERSION = 0.2

if __name__ == '__main__':
    # argument parser
    parser = argparse.ArgumentParser(description=DESCRIPTION, epilog='Version: {VERSION}')
    parser.add_argument('-cw', '--center_wavelength', help='Center wavelength (nm)', type=float, default=1064)
    parser.add_argument('-strw', '--start_wavelength', help='Start wavelength (nm)', type=float, default=1061.5)
    parser.add_argument('-stpw', '--stop_wavelength', help='Stop wavelength (nm)', type=float, default=1066.5)
    parser.add_argument('-sen', '--sensitivity', help='Sensitivity', type=str, default="MID")
    parser.add_argument('-res', '--resolution', help='Resolution (pm)', type=float, default=20)
    parser.add_argument('-fib', '--fiber_type', help='Fiber type', type=str, default="LARGE")
    parser.add_argument('-pts', '--measurement_pts', help='Measurement points', type=int, default=5001)
    parser.add_argument('-lev', '--ref_level', help='Reference level (dBm)', type=int, default=-20)
    parser.add_argument('-sm', '--sweep_mode', help='Sweep mode', type=str, default="SINGLE")
    parser.add_argument('-th', '--threshold', help='Threshold (dB)', type=int, default=3)
    parser.add_argument('-int', '--meas_interval', help='Measurement interval (s)', type=int, default=300)


    args = parser.parse_args()

    rm = visa.ResourceManager()
    Yokogawa = rm.open_resource("TCPIP0::192.168.10.100::inst0::INSTR")
    Yokogawa.timeout = 20000000
    Yokogawa.clear()
    # =========================================================
    # Initialize YOKOGAWA AQ6373B
    # =========================================================
    initialize()

    CENTER_WAVELENGTH = args.center_wavelength
    START_WAVELENGTH = args.start_wavelength
    STOP_WAVELENGTH = args.stop_wavelength
    SENSITIVITY = args.sensitivity
    RESOLUTION = args.resolution
    FIBER_TYPE = args.fiber_type
    MEASUREMENT_POINTS = args.measurement_pts
    REFERENCE_LEVEL = args.ref_level
    SWEEP_MODE = args.sweep_mode
    THRESHOLD =  args.threshold
    MEA_INTERVAL =  args.meas_interval

    # =========================================================
    # Settimg parameters
    # =========================================================
    set_parameters()

    i = 0 #current number of measurement
    file_name = "KPS_SN2102288" #file_name
    t_interval = MEA_INTERVAL #interval between measurement
    t_elapsed = 0 #curremt measuremet time (sec)
    t_elapsed_round = 0
    hour = 0 #curremt measuremet time (h)
    hour_round = 0
    # =========================================================
    # Data logging
    # =========================================================
    print("Start data logging ... (Press Ctrl+C to stop)\n")
    with open('spectrum_log.csv', 'w') as logfile:
        logfile.write("#%s" % do_query_string("*IDN?"))
        logfile.write("#Start datetime:, %s\n" % datetime.datetime.now())
        logfile.write("#Center WL:, %e nm\n" % CENTER_WAVELENGTH)
        logfile.write("#Start WL:, %e nm\n" % START_WAVELENGTH)
        logfile.write("#Stop WL:, %e nm\n" % STOP_WAVELENGTH)
        logfile.write("#Sensitivity:, %s\n" % SENSITIVITY)
        logfile.write("#Resolution:, %e pm\n" % RESOLUTION)
        logfile.write("#Fiber type:, %s \n" % FIBER_TYPE)
        logfile.write("#Measurement points:, %e \n" % MEASUREMENT_POINTS)
        logfile.write("#Reference level:, %e dBm\n" % REFERENCE_LEVEL)
        logfile.write("#Sweep mode:, %s \n" % SWEEP_MODE)
        logfile.write("#Threshold:, %e dB\n" % THRESHOLD)
        logfile.write("#Measurement interval:, %e s\n" % MEA_INTERVAL)
        logfile.write("#Time_elapsed(s), \n")

        try:
            while True:
                t1 = time.time() #sec
                #do sweep
                print(f"cycle no. {i+1} started")
                do_sweep()
                wait()

                #analysis bandwidth
                cal_bandwidth()

                #Get data
                x = get_x_data()
                y = get_y_data()

                #register wavelength at the initial measurement i = 0
                if i == 0:
                    logfile.write(f"Temperature (¡æ), {x}")
                    #logfile.write(f"T = {hour_round} (h),{y}")
                    logfile.write(f"{hour_round},{y}")
                else:
                    logfile.write(f"{hour_round},{y}")
    
                #save data to USB
                #file name: 000i
                number = str(i+1).zfill(4)
                save(f'{file_name}{number}')

                sleep(t_interval)
                t2 = time.time() #sec
                t_elapsed += t2 - t1
                t_elapsed_round = round(t_elapsed, 3)
                #convert sec to hour
                hour = t_elapsed / 60 / 60
                hour_round = round(hour, 3)
                print(f"Elapsed time: {t_elapsed_round} s, ({hour_round} h)")
                i += 1

        except KeyboardInterrupt:
            print("Measurement stoped at %.3f s\n" %(t_elapsed))
    # =========================================================
    # Close program
    # =========================================================
    Yokogawa.close()
    print("YOKOGAWA AQ6373B closed!")

    sys.exit()