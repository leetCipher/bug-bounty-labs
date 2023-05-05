#!/usr/bin/python3
import base64
import base58
import sys
import re


def main(file, domain):
	handle = open(file, "r")
	logs = handle.read().strip()

	payload = re.findall(r"\[(.*)\." + domain + "]", logs)
	payload = list(dict.fromkeys(payload))
	payload = "".join(payload)
	decoded_data = base58.b58decode(payload)
	decoded_data = base64.b64decode(decoded_data).decode("UTF-8")

	decoded_file_handle = open("decoded-payload.txt", "w")
	decoded_file_handle.write(decoded_data)
	handle.close()
	decoded_file_handle.close()


if __name__ == "__main__":
	if len(sys.argv) == 3:
		main(sys.argv[1], sys.argv[2])
	else:
		print("usage: <logs-file> <domain>")