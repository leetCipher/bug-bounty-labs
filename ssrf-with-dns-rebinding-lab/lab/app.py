from flask import Flask, request, render_template, redirect, make_response, jsonify
import requests
import hashlib
import socket
import urllib
import time
import os

# init Flask
app = Flask(__name__)


@app.route("/", methods = ["GET"])
def main():
	if request.cookies.get('uuid_hash') == None:
		return redirect("/login", code = 302)
	return render_template("index.html"), 200


@app.route("/api/v3/login", methods = ["POST"])
def check_creds():
	# form post data
	username = request.form.get("username")
	password = request.form.get("password")

	# check creds
	if username == "h4ck3r" and password == "p@55w0rd":
		res = make_response(redirect("/", code = 302))
		res.set_cookie("uuid_hash", hashlib.sha512(b"5d59daf3-f7cb-4a79-8c69-ec657aebb89a").hexdigest())
		return res
	else:
		return "dude, the correct credentials are literally in front of you!", 401


@app.route("/login", methods = ["GET"])
def login():
	# check if user cookie is already set
	user_uuid_hash = request.cookies.get('uuid_hash')
	if user_uuid_hash != None:
		if user_uuid_hash == hashlib.sha512(b"5d59daf3-f7cb-4a79-8c69-ec657aebb89a").hexdigest():
			return redirect("/", code = 302)
		else:
			return render_template("login.html")
	else:
		return render_template("login.html")


@app.route("/logout", methods = ["GET"])
def logout():
	# delete user cookie and redirect to login page
	res = make_response(redirect("/login", code = 302))
	res.delete_cookie("uuid_hash")
	return res


@app.route("/api/v3/users", methods = ["POST"])
def get_user_files():
	try:
		user_uuid = request.get_json()["user_uuid"]
		if user_uuid != None:
			if user_uuid == "5d59daf3-f7cb-4a79-8c69-ec657aebb89a":
				user_files = os.listdir("users/5d59daf3-f7cb-4a79-8c69-ec657aebb89a/")
				return jsonify(user_files)
			return "invalid uuid", 401
		else:
			return "invalid uuid", 401
	except:
		return "invalid uuid", 401


@app.route("/api/v3/upload", methods = ["POST"])
def upload_files_via_url_v3():
	# check if user is logged in
	uuid_hash = request.cookies.get("uuid_hash")
	if uuid_hash == None:
		return redirect("/login", code = 302)
	# block all requests to localhost
	file_url = request.form.get("file_url")
	try:
		file_domain = file_url.split("/")[2].split(":")[0]
		request_ip = socket.gethostbyname(file_domain)
		if request_ip.startswith("127") or \
		request_ip.startswith("0") or \
		request_ip.startswith("192"):
			return "invalid url\n", 403
		file_name = file_url.split("/")[-1]
		file_contents = requests.get(file_url).text
		fd = open(f"users/5d59daf3-f7cb-4a79-8c69-ec657aebb89a/{file_name}", "w")
		fd.write(file_contents)
		fd.close()
		return file_contents
	except:
		return "invalid url\n", 403


@app.route("/api/v2/upload", methods = ["POST"])
def upload_files_via_url_v2():
	uuid_hash = request.cookies.get("uuid_hash")
	if uuid_hash == None:
		return redirect("/login", code = 302)
	content_type = request.headers.get("Content-Type")
	# block all requests to localhost
	if content_type == "application/x-www-form-urlencoded":
		try:
			file_url = request.form.get("file_url")
			file_domain = file_url.split("/")[2].split(":")[0]
			request_ip = socket.gethostbyname(file_domain)
			if request_ip.startswith("127") or \
			request_ip.startswith("0") or \
			request_ip.startswith("192"):
				return "invalid url\n", 403
			file_name = file_url.split("/")[-1]
			file_contents = requests.get(file_url).text
			fd = open(f"users/5d59daf3-f7cb-4a79-8c69-ec657aebb89a/{file_name}", "w")
			fd.write(file_contents)
			fd.close()
			return file_contents
		except:
			return "invalid url\n", 403
	else:
		try:
			file_url = urllib.parse.unquote(request.get_json()["file_url"])
			file_domain = file_url.split("/")[2].split(":")[0]
			request_ip = socket.gethostbyname(file_domain)
			if request_ip.startswith("127") or \
			request_ip.startswith("0") or \
			request_ip.startswith("192"):
				return "requests to localhost not allowed\n", 403
			time.sleep(1)
			headers = {"X-Request-Ip": "127.0.0.1"}
			res = requests.get(file_url, headers = headers)
			file_contents = res.text
			status_code = res.status_code
			return file_contents, status_code
		except:
			return "requests to localhost not allowed\n", 403


@app.route("/api", methods = ["GET", "POST"])
def api_docs():
	# only accessible from localhost
	request_src_ip = request.headers.get("X-Request-Ip")
	if request_src_ip == None or request_src_ip != "127.0.0.1":
		return "Not Found", 404

	return """/users
	/status
	/employees
	""", 200


@app.route("/api/users", methods = ["GET", "POST"])
def get_users_uuids():
	# only accessible from localhost
	request_src_ip = request.headers.get("X-Request-Ip")
	if request_src_ip == None or request_src_ip != "127.0.0.1":
		return "Not Found", 404

	# get user files
	user_uuid = request.args.get("uuid")
	if user_uuid != None:
		user_files = os.listdir(f"users/{user_uuid}/")
		return jsonify(user_files)
	else:
		# get all users uuids
		users = os.listdir("users/")
		return jsonify(users)


@app.route("/api/status", methods = ["GET", "POST"])
def get_site_status():
	# only accessible from localhost
	request_src_ip = request.headers.get("X-Request-Ip")
	if request_src_ip == None or request_src_ip != "127.0.0.1":
		return "Not Found", 404
	return "site is up", 200


@app.route("/api/employees", methods = ["GET", "POST"])
def get_employees():
	# only accessible from localhost
	request_src_ip = request.headers.get("X-Request-Ip")
	if request_src_ip == None or request_src_ip != "127.0.0.1":
		return "Not Found", 404
	return "we currently have 1337 active employees"


@app.errorhandler(404)
def page_not_found(e):
	return "resource not found", 404


if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 80)

