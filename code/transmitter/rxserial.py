# rxserial.py C.Wagner 9.11.23
import socket
import struct
import sys
import serial

ser = serial.Serial("/dev/serial0",
      250000,
      bytesize=serial.EIGHTBITS,
      parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_TWO,
      timeout=5)

data = ser.read(1024)
print(data)



