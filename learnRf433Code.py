#!/usr/bin/env python
import socket
import sys
import binascii
import struct

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcastIp = ('255.255.255.255', 9001)
SOF = b'\xff\xee'
EOF = b'\xef\xfe'
INIT = b'\x11\x00\x00\x11'
TV_POWER = b'\xd1\x71\x00\x00\x00\x00\x00\x2d\x04\x88\x06\x44\x00\xaa\x00\x13\x00\xac\x00\x41\x00\x16\x06\xf6\x04\x02\x13\x14\x15\x06\x01\x11\x22\x21\x12\x13\x01\x22\x31\x22\x24\x22\x33\x11\x50\x12\x23\x12\x22\x42\x23\x31\x11\x23'
LEARN_IR = b'\xb1\x11\x00\x00\x00\x05\x00\x00\x00\x00\x20\xe7'
LEARN_RF = b'\xb3\x10\x00\x00\x00\x05\x00\x00\x00\x00\x20\xe8'
RF_SOF = b'\xd3\x11\x00\x00\x00\x00\x00'
try:

    # Send data
    print >>sys.stderr, 'sending "%s"' % binascii.hexlify(INIT)
    sent = sock.sendto(SOF+INIT+EOF, broadcastIp)

    # Receive response
    print >>sys.stderr, 'waiting to receive'
    data, server = sock.recvfrom(4096)
    print('Received %r from %s' % (binascii.hexlify(INIT), server))
    
     # Send data
    print >>sys.stderr, 'sending "%s"' % binascii.hexlify(LEARN_IR)
    sent = sock.sendto(SOF+LEARN_RF+EOF, server)
    
    # Receive response
    print >>sys.stderr, 'waiting to receive'
    data, server = sock.recvfrom(4096)
    print('Received Raw %r from %s' % (binascii.hexlify(data), server))
    RF_PAYLOAD=data[7:]
    print('RF CODE01 %s' % binascii.hexlify(RF_PAYLOAD))
    RF_PAYLOAD=RF_PAYLOAD[:-2]
    print('RF CODE02 %s' % binascii.hexlify(RF_PAYLOAD))
    RF_PAYLOAD_LAST= bytearray(RF_PAYLOAD[-1:])[0]
    RF_PAYLOAD=RF_PAYLOAD[:-1]
    print('RF CODE03 %s' % binascii.hexlify(RF_PAYLOAD))
    print(RF_PAYLOAD_LAST)
    RF_PAYLOAD_LAST+=31
    print(RF_PAYLOAD_LAST)
    ##RF_PAYLOAD_LAST=RF_PAYLOAD_LAST
    RF_PAYLOAD_FINAL = RF_SOF + bytearray(RF_PAYLOAD) + bytes(chr(RF_PAYLOAD_LAST))
    print('RF_PAYLOAD_FINAL %s' % binascii.hexlify(RF_PAYLOAD_FINAL))
    
except:
        print("Oops!",sys.exc_info()[1],"occured.")
finally:
    print >>sys.stderr, 'closing my socket'
    sock.close()
    sys.exit(0)
