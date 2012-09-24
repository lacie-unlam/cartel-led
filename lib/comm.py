import serial

device = '/dev/ttyUSB0'

def write(data):
    ser = serial.Serial(device, 9600, timeout=0.5)
    ser.write(data)
    ser.close()