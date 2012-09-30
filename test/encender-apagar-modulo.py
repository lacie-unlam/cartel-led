#!/usr/bin/python

import serial
import time

# ser = serial.Serial('/dev/ttyUSB0', baudrate=19200)
ser = serial.Serial('/dev/ttyS0', baudrate=19200)

PARPADEOS = 5
MODULOS = 8

for i in ['FFFF', 'AA55', '55AA', 'F0F0', 'OF0F', 'FF00', '00FF']:
    for j in PARPADEOS:
        for n in range(MODULOS):
            ser.write("zg0000\r")
            ser.write("zh0000\r")
            ser.write("zi0000\r")
            ser.write("zj0000\r")
            ser.write("zs\r")
            time.sleep(0.01)
        ser.write("zm\r")

        time.sleep(0.25)

        for n in range(MODULOS):
            ser.write("zg%s\r" % i)
            ser.write("zh%s\r" % i)
            ser.write("zi%s\r" % i)
            ser.write("zj%s\r" % i)
            ser.write("zs\r")
            time.sleep(0.01)
        ser.write("zm\r")

        time.sleep(0.5)

ser.close()
