from flask import Flask, request, render_template, redirect
from string import ascii_lowercase, digits
import redis
import random
import re

# init Flask
app = Flask(__name__)
# init redis
redis_db = redis.Redis('redis_db')

@app.route("/", methods = ["GET"])
def check_permissions():
	auth_token = request.headers.get("X-Authorized-For")
	# validate the "X-Authorized-For" header
	if auth_token == None or len(auth_token) != 40:
		return render_template("forbidden.html"), 403
	else:
		# check if the authorization token is expired
		logs_fd = open("logs/admin_logs", "r")
		logs = logs_fd.read().strip()
		logs_fd.close()
		expired_tokens = re.findall(r"X-Authorized-For: ([a-z0-9]{40})", logs)
		if auth_token in expired_tokens:
			return render_template("token-expired.html"), 403

		# check if the authorization token is set
		if redis_db.get(auth_token) == None:
			return render_template("forbidden.html"), 403

		return render_template("admin-login.html")


@app.route("/request_otp", methods = ["POST"])
def request_otp():
	# check if email is supplied
	email = request.form.get("email")
	if email == None:
		return render_template("email-not-allowed.html"), 401
		
	# check if the supplied email is allowed
	is_email_allowed = re.match(r"^.*@vulnerable\.com$", email)
	if not bool(is_email_allowed):
		return render_template("email-not-allowed.html"), 401

	# validate the "X-Authorized-For" header
	auth_token = request.headers.get("X-Authorized-For")
	if auth_token == None or len(auth_token) != 40:
		return render_template("forbidden.html"), 403

	# check if the authorization token is stored in redis or not
	if redis_db.get(auth_token) == None:
		return render_template("forbidden.html"), 403

	# generate the OTP and store it in redis
	if redis_db.get("otp") == None:
		redis_db.set("otp", "".join(random.choices(digits, k = 4)))

	# log the authorization token to the logs file
	logs_fd = open("logs/admin_logs", "a")
	logs_fd.write("X-Authorized-For: {}\n".format(auth_token))
	logs_fd.close()
	
	return render_template("submit-otp.html")


@app.route("/submit_otp", methods = ["POST"])
def check_otp():
	auth_token = request.headers.get("X-Authorized-For")
	# validate the "X-Authorized-For" header
	if auth_token == None or len(auth_token) != 40:
		return render_template("forbidden.html"), 403
	
	# check if the authorization token is stored in redis or not
	if redis_db.get(auth_token) == None:
		return render_template("forbidden.html"), 403

	# check if the OTP is set or not
	if redis_db.get("otp") == None:
		return render_template("forbidden.html"), 403

	# check if the supplied OTP matches the one stored in redis
	otp = request.form.get("otp")
	if otp == redis_db.get("otp").decode("UTF-8"):
		# if the OTPs match, set admin signature in redis and redirect to admin dashboard
		redis_db.set(f"{auth_token}_{otp}", "1")
		return redirect("/admin_dashboard", code = 302)
	else:
		# if the OTPs don't match delete all keys in redis and redirect to invalid_otp page
		redis_db.delete(auth_token)
		return render_template("invalied-otp.html"), 401


@app.route("/admin_dashboard", methods = ["GET"])
def admin_dashboard():
	auth_token = request.headers.get("X-Authorized-For")
	# validate the "X-Authorized-For" header
	if auth_token == None or len(auth_token) != 40:
		return render_template("forbidden.html"), 403

	# check if the authorization token is stored in redis or not
	if redis_db.get(auth_token) == None:
		return render_template("forbidden.html"), 403

	# check if the OTP is set or not
	if redis_db.get("otp") == None:
		return render_template("forbidden.html"), 403
		
	# get the otp from redis
	otp = redis_db.get("otp").decode("UTF-8")
	
	# check for admin signature
	if redis_db.get(f"{auth_token}_{otp}") == None:
		return render_template("forbidden.html"), 403

	# set expiry date for all keys
	redis_db.expire(auth_token, 660)
	redis_db.expire("otp", 660)
	redis_db.expire(f"{auth_token}_{otp}", 660)

	# render admin dashboard
	return render_template("admin-dashboard.html")


@app.route("/logs", methods = ["GET"])
def forbidden():
	return render_template("forbidden.html"), 403


@app.route("/logs/admin_logs", methods = ["GET"])
def show_admin_logs():
	# show the admin logs
	logs_fd = open("logs/admin_logs", "r")
	logs = logs_fd.read().strip().split("\n")
	return render_template("display-logs.html", logs = logs)


@app.route("/api/request/auth_token", methods = ["POST"])
def generate_auth_token():
	# generate authorization token
	auth_token = "".join(random.choices(ascii_lowercase + digits, k = 40))

	# store the generated authorization token in redis
	redis_db.set(auth_token, "1")
	return auth_token


if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 5000)
