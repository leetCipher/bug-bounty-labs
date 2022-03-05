#!/usr/bin/python3
import hashlib
import sys


def main(first_name, last_name):
	# hashes wordlist
	wordlist_fd = open("hashes-wordlist.txt", "w")
	# user full name reversed
	full_name = first_name + last_name
	full_name = full_name[::-1]

	# brute-force all dates since 2017
	for year in range(2017, 2022, 1):
		for month in range(1, 13):
			for day in range(1, 32):
				string = "{}{:02}{:02}{}".format(full_name, day, month, year)
				# generate the SHA-256 sum of the reversed full name and the date
				hashed_string = hashlib.sha256(string.encode()).hexdigest()
				
				# write the hash to the hashes-wordlist.txt file
				wordlist_fd.write("{}\n".format(hashed_string))

	# close the fd
	wordlist_fd.close()
	print("[+] wordlist generated for {} {}".format(first_name, last_name))


if __name__ == "__main__":
	if len(sys.argv) == 3:
		main(str(sys.argv[1]), str(sys.argv[2]))
	else:
		print("usage: ./generate-hashes.py <first-name> <last-name>")