import serial

def write(data):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5)
    ser.write(data)
    ser.close()