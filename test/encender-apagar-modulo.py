#!/usr/bin/python

import serial
import time

# class serial.Serial
# __init__(port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE, 
#          timeout=None, xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False, interCharTimeout=None)

ser = serial.Serial('/dev/ttyUSB0', timeout=0.5)
# encender todo un modulo
ser.write('zr (\r\n)')
ser.write('zgFFFF (\r\n)')
ser.write('zgFFFF (\r\n)')
ser.write('zs (\r\n)')
ser.write('zm (\r\n)')

time.sleep(2)

# apagar todo un módulo
ser.write('zr (\r\n)')
ser.write('zg000 (\r\n)')
ser.write('zg000 (\r\n)')
ser.write('zs (\r\n)')
ser.write('zm (\r\n)')

ser.close()

# 8n1 (8 bits de datos, sin paridad 1 es el stop bit)