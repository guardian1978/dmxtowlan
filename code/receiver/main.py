import WIFI_CONFIG
from network_manager import NetworkManager
import uasyncio
import socket
import struct
import sys
import urequests
import time
import utime
from machine import Pin, Timer

led = Pin("LED", Pin.OUT)
tim = Timer()

def status_handler(mode, status, ip):
    # reports wifi connection status
    led.value(0)
    print(mode, status, ip)
    print('Connecting to wifi...')
    led.value(1)
    if status is not None:
        if status:
            print('Connection successful!')
            led.value(1)
        else:
            print('Connection failed!')
            led.value(0)

def inet_aton(addr):
    ip_as_bytes = bytes(map(int, addr.split(".")))
    return ip_as_bytes

def tick(timer):
    global led
    led.toggle()
    
# set up wifi
network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))


message = "Hallo1"
multicast_group = '224.0.0.0'
multicast_port = 5007
MULTICAST_TTL = 1

# The first step to establishing a multicast receiver is to create 
# the UDP socket.
server_address = ('224.0.0.0', 5007)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to 
# the multicast group on all interfaces.
group = inet_aton(multicast_group)
try:
    mreq = struct.pack('4sL', group, 0) #socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
except:
        print("Missed to join Multicast Group!")


# Receive/respond loop
while True:
    print ('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)
    
    led.value(0)
    tim.init(mode=Timer.ONE_SHOT, period = 200, callback = tick)
    
    print ('received %s bytes from %s' % (len(data), address))
    print (data)

    print ('sending acknowledgement to', address)
    sock.sendto('ack', address)
    
