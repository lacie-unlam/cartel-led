import serial
import time
import logging
import os

import lib.logger
from iter import in_groups
from lib.estructuras import Matriz
from lib import null

class Serializer:
    device = '/dev/ttyUSB0'
    
    def __init__(self, matriz):
        self.matriz = matriz
        if os.path.exists(self.device):
            self.ser = serial.Serial(self.device, baudrate=19200)
        else:
            self.ser = null.Null()

    def write(self):
        from ui.widgets import ModuloLeds

        for m in range(self.matriz.columnas/ModuloLeds.CANT_LEDS_X_FILA):
            for r in range(self.matriz.filas/ModuloLeds.CANT_LEDS_X_COL):
                reg = chr(ord('g') + r)
                bytes, cols = [], ModuloLeds.CANT_LEDS_X_COL/2
                for c in range(cols):
                    bytes.append([self.matriz[i+2*c+ModuloLeds.CANT_LEDS_X_COL*r, j+ModuloLeds.CANT_LEDS_X_FILA*m] 
                                    for i in range(cols)
                                    for j in range(ModuloLeds.CANT_LEDS_X_FILA)])
                    # b = []
                    # for i in range(cols):
                    #     for j in range(ModuloLeds.CANT_LEDS_X_FILA):
                    #         print 'f:', i+2*c+ModuloLeds.CANT_LEDS_X_COL*r
                    #         print 'c:', j+ModuloLeds.CANT_LEDS_X_FILA*m
                    #         b.append(self.matriz[i+2*c+ModuloLeds.CANT_LEDS_X_COL*r, j+ModuloLeds.CANT_LEDS_X_FILA*m])
                    # bytes.append(b)
                self.write_bytes(bytes, reg)
        
            self.ser.write("zs\r")
            logging.info('zs')
            time.sleep(0.01)
        self.ser.write('zm\r')
        logging.info('zm')

    def write_bytes(self, bytes, r):
        for bits in reversed(bytes):
            hexa = ''.join(map(lambda x: '1' if x else '0', bits))
            data = hex(int(hexa, 2))[2:]
            logging.info('z%s: %s', r, data.rjust(4, '0'))
            self.ser.write('z%s%s\r' % (r, data.rjust(4, '0')))

    def __del__(self):
        self.ser.close()