import IP2Location
import os
import struct
import socket
database = IP2Location.IP2Location(os.path.join("ip2loc.BIN"))

f = open('ip2loc.BIN', 'rb')

print(f)


_ipv4indexbaseaddr = struct.unpack('<I', f.read(4))[0]

print("Base Address -> {}".format(_ipv4indexbaseaddr))




ipno = struct.unpack('!L', socket.inet_pton(socket.AF_INET, '192.168.1.1'))[0]
print("IO Number ->  {}".format(ipno))

indexpos = ((ipno >> 16) << 3) + _ipv4indexbaseaddr

f.seek(indexpos - 1)

print( struct.unpack('<I', f.read(4))[0])

n = struct.unpack('B',f.read(1))[0]


print(str(f.read(n).decode('iso-8859-1').encode('utf-8')))


f.close