const mysql = require("mysql2");

const connection = mysql.createConnection({
	host: "mysql_database",
	user: "root",
	password: "R007P@55W0RD123",
	database: "vuln_platform"
});

module.exports = connection;