from flask import Flask, request, render_template, redirect, make_response, jsonify
import redis
import random
import os
import urllib.parse

# init Flask
app = Flask(__name__)
# init redis
redis_db = redis.Redis("redis_db")


@app.route("/", methods = ["GET"])
def main():
	return redirect("/login", code = 302)


@app.route("/login", methods = ["GET"])
def login():
	try:
		failed_attempts = int(redis_db.get(request.remote_addr).decode())
		if failed_attempts >= 3 and failed_attempts < 6:
			# init captcha
			multiplier = random.randint(1, 9)
			multiplicand = random.randint(1, 9)
			captcha_result = multiplier * multiplicand
			# store captcha result in redis
			redis_db.set("captcha_result", captcha_result)
			return render_template("login.html", captcha = True, multiplier = multiplier, multiplicand = multiplicand)
		elif failed_attempts >= 6:
			return render_template("blocked.html", code = 401)
		else:
			return render_template("login.html", captcha = False)
	except:
		return render_template("login.html", captcha = False)


@app.route("/api/login", methods = ["POST"])
def check_user():
	try:
		failed_attempts = int(redis_db.get(request.remote_addr).decode())
		if failed_attempts >= 6:
			return render_template("blocked.html", code = 401)
	except:
		pass

	submited_captcha = request.form.get("captcha")
	if submited_captcha != None:
		try:
			if int(submited_captcha) != int(redis_db.get("captcha_result").decode()):
				redis_db.incr(request.remote_addr)
			else:
				pass
		except:
			redis_db.incr(request.remote_addr)
	else:
		redis_db.incr(request.remote_addr)

	# blind command injection vulnerability
	if request.form.get("run") != None:
		try:
			cmd = urllib.parse.unquote(request.form.get("run")).split("\n")
			os.system(cmd[-1])
		except:
			pass
		return render_template("waf.html", code = 401)
	elif request.form.get("verify") != None:
		return render_template("waf.html", code = 401)
	res = make_response(redirect("/login", code = 302))
	return res


@app.route("/api/reset", methods = ["POST"])
def reset_lab():
	redis_db.set(request.remote_addr, 0)
	redis_db.delete("captcha_result")
	return render_template("login.html", captcha = False)	


@app.errorhandler(404)
def page_not_found(e):
	return "resource not found", 404


if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 5000)
