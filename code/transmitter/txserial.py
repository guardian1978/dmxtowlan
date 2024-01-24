# rxserial.py C.Wagner 9.11.23
import socket
import struct
import sys
import serial

x = 0

#ser = serial.Serial("/dev/serial0",
ser = serial.Serial("/dev/ttyUSB0",
      250000,
      bytesize=serial.EIGHTBITS,
      parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE)

while x<512:
  ser.write(x)
  x = x + 1

ser.close()



