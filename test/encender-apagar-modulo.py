#!/usr/bin/python

import serial
import time

# ser = serial.Serial('/dev/ttyUSB0', baudrate=19200)
ser = serial.Serial('/dev/ttyS0', baudrate=19200)

PARPADEOS = 5
MODULOS = 7
ZS_TIME = 0.01
OFF_TIME = 0.1
ON_TIME = 0.05

for i in ['FFFF', '00FF', 'AA55', '55AA', 'F0F0', 'FF00']:
    for j in range(PARPADEOS):
        for n in range(MODULOS*2):
            ser.write("zg0000\r")
            ser.write("zh0000\r")
            ser.write("zi0000\r")
            # ser.write("zj0000\r")
            ser.write("zs\r")
            time.sleep(ZS_TIME)
        ser.write("zm\r")
        time.sleep(OFF_TIME)

        for n in range(MODULOS*2):
            ser.write("zg%s\r" % i.rjust(4, '0'))
            ser.write("zh%s\r" % i.rjust(4, '0'))
            ser.write("zi%s\r" % i)
            # ser.write("zj%s\r" % i)
            ser.write("zs\r")
            time.sleep(ZS_TIME)
        ser.write("zm\r")
        time.sleep(ON_TIME)

ser.close()
