# send.py C.Wagner 9.11.23
import socket
import struct
import sys


message = b"Hallo"
multicast_group = '224.0.0.0'
multicast_port = 5007
MULTICAST_TTL = 2

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)


# Set a timeout so the socket does not block indefinitely when trying
# to receive data. (in sec flaot)
sock.settimeout(1.0)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

count = 0

try:        
    # Send data to the multicast group
    print('sending "%s"' % message) #, sys.stderr)
    sent = sock.sendto(message, (multicast_group, multicast_port))
    count = 0

    # Look for responses from all recipients
    while True:
        print('waiting to receive') #, sys.stderr)
        print("Got answers from %d receivers." % (count))
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('timed out, no more responses') #, sys.stderr)
            break
        else:
            print('received "%s" from %s' % (data, server)) #, sys.stderr)
            count = count + 1
            
finally:
    print('closing socket') #, sys.stderr)
    sock.close()
