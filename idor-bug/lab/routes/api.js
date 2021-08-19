const express = require("express");
const redis = require("redis");
const crypto = require("crypto");
const mysqlDB = require("../db.js");
const router = express.Router();
const client = redis.createClient({host: "redis-server", port: 6379});


const registerUser = (first_name, last_name, email, password, user_hash) => {
	// get the SHA1 sum of the password
	let passwordHash = crypto.createHash("sha1").update(password).digest("hex");

	// insert data to database
	let insertDataQuery = "INSERT INTO users (first_name, last_name, email, password, user_hash, phone_number, address, access_token, birth_place, posts_count, joined_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
	let values = [first_name, last_name, email, passwordHash, user_hash, "+0123456789", "21 jump street", "N07_SUP3R_S3CR37_4CC355_70K3N", "somewhere on earth", 0, "2021"];

	// insert data into database
	mysqlDB.query(insertDataQuery, values, (err, result) => {
		if (err) throw err
	});
}


router.post("/user", (req, res) => {
	const blacklistedFuzzers = ["python-requests", "Wfuzz", "Fuzz Faster"];
	// check if user is logged in
	if (req.headers.cookie === undefined || req.headers.cookie.split(";")[0].split("=")[0] !== "auth" || req.headers.cookie.split(";")[0].split("=")[1].length !== 64) {
		res.status(401);
		res.send("Invalid auth cookie");
	// check for fuzzing tools or python-requests module
	} else if (req.headers["user-agent"].substring(0, blacklistedFuzzers[0].length) === blacklistedFuzzers[0] ||
			   req.headers["user-agent"].substring(0, blacklistedFuzzers[1].length) === blacklistedFuzzers[1] ||
			   req.headers["user-agent"].substring(0, blacklistedFuzzers[2].length) === blacklistedFuzzers[2]) {
				res.status(403);
				res.send("bot detected");
	} else {
		// get client's referer header if exists, if not get the client's ip address
	    let requestRefererOrIP = req.headers.referer !== undefined ? req.headers.referer : req.connection.remoteAddress;

	    // insert client referer header in redis
	    client.incr(requestRefererOrIP);

	    // init requests counter
	    let requestsCount = 0;
	    client.get(requestRefererOrIP, (err, reply) => {
	        requestsCount = parseInt(reply);
	        if (requestsCount === 1) {
	        	// set requester referer header expire date after 5 minutes
	            client.expire(requestRefererOrIP, 300);

				// extract user hash
				let userHash = req.body.user_hash;

				// get user data
				let fetchUserDataQuery = "SELECT * FROM users WHERE user_hash = ?";
				mysqlDB.query(fetchUserDataQuery, userHash, (err, data) => {
					if (data.length === 1) {
						delete data[0].password;
						res.json(data[0]);
					} else {
						res.status(404);
						res.send("Invalid user hash");
					}
				});

	        } else if (requestsCount > 20) {
	        	// too many requests
	            res.status(429);
	            res.send("Too many requests, wait for 5 minutes to make requests again");

	        } else {
				// extract user hash
				let userHash = req.body.user_hash;

				// get user data
				let fetchUserDataQuery = "SELECT * FROM users WHERE user_hash = ?";
				mysqlDB.query(fetchUserDataQuery, userHash, (err, data) => {
					if (data.length === 1) {
						delete data[0].password;
						res.json(data[0]);
					} else {
						res.status(404);
						res.send("Invalid user hash");
					}
				});
	        }
	    });
	}
});

router.post("/register", (req, res) => {
	// extract post data
	let {first_name, last_name, email, password, user_hash} = req.body;

	// check if email is already registered
	let emailCheckQuery = "SELECT email FROM users WHERE email = ?";
	mysqlDB.query(emailCheckQuery, email, (err, row) => {
		if (err) throw err;
		if (row.length === 1) {
			res.status(409);
			res.send("email is already registered");
		} else {
			// register user
			registerUser(first_name, last_name, email, password, user_hash);

			// send 200 OK if everything went fine and redirect to login page
			res.status(200);
			res.send("registered successfully!");
		}
	});
});

router.post("/login", (req, res) => {
	// extract post data
	let {email, password} = req.body;

	// get the SHA1 sum of the password
	let passwordHash = crypto.createHash("sha1").update(password).digest("hex");

	// check if user exists
	let query = "SELECT email, password, user_hash FROM users WHERE email = ? AND password = ?";
	let values = [email, passwordHash];
	mysqlDB.query(query, values, (err, row) => {
		if (err) throw err;
		if (row.length > 0) {
			// create a dummy cookie and set it as auth cookie and redirect to homepage
			let authCookie = crypto.createHash("sha256").update(row[0]["password"] + row[0]["user_hash"]).digest("hex");
			res.cookie("auth", authCookie, {maxAge: 90000000})
			res.cookie("user_hash", row[0]["user_hash"], {maxAge: 90000000})
			res.status(302);
			res.redirect("/")
		} else {
			res.status(404);
			res.send("user does not exist");
		}
	});
});


module.exports = router;