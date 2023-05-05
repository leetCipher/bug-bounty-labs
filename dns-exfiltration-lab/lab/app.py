from flask import Flask, render_template, request
import subprocess
import os
import re

# init Flask
app = Flask(__name__)

authorized_ports = [
    49335, 49336, 49337, 49338, 49339,
    49340, 49341, 49342, 49343, 49344,
    49345, 49346, 49347, 49348, 49349,
    49350, 49351, 49352, 49353, 49354
]

ptr = 0

@app.route("/", methods = ["GET"])
def main():
    up = False
    return render_template("index.html"), 200


@app.route("/check-status", methods = ["POST"])
def check_status():
    global authorized_ports, ptr
    site = request.form.get("site")
    pattern = r"^[a-z\-\d]+\.[a-z]+$"
    match = re.match(pattern, site)
    if match:
        result = subprocess.run([
            "curl", "--head", "--local-port", str(authorized_ports[ptr]), "--connect-timeout", "5", site
            ], capture_output = True, text = True).stdout
        ptr = (ptr + 1) % len(authorized_ports)
        if result == "":
            return render_template("status.html", up = False), 200
        else:
            return render_template("status.html", up = True), 200
    else:
        re.sub(r":\d{1,5}", "", site)
        os.system(f"echo {site}")
        return render_template("error.html"), 400


if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 80)
