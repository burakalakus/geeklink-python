#!/usr/bin/env python
import socket
import sys
import binascii

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcastIp = ('255.255.255.255', 9001)
SOF = b'\xff\xee'
EOF = b'\xef\xfe'
INIT = b'\x11\x00\x00\x11'

try:

    # Send data
    print >>sys.stderr, 'sending "%s"' % binascii.hexlify(INIT)
    sent = sock.sendto(SOF+INIT+EOF, broadcastIp)

    # Receive response
    print >>sys.stderr, 'waiting to receive'
    data, server = sock.recvfrom(4096)
    print('Received %r from %s' % (binascii.hexlify(data), server))
    
     # Send data
    print >>sys.stderr, 'sending "%s"' % sys.argv[1]
    sent = sock.sendto(SOF+binascii.unhexlify(sys.argv[1])+EOF, server)
    
    # Receive response
    print >>sys.stderr, 'waiting to receive'
    data, server = sock.recvfrom(4096)
    print('Received %r from %s' % (binascii.hexlify(data), server))
	


finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
    sys.exit(0)
