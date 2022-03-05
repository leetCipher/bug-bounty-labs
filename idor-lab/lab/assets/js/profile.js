const firstName = document.getElementById("first_name");
const lastName = document.getElementById("last_name");
const email = document.getElementById("email");
const phoneNum = document.getElementById("phone_number");
const accessToken = document.getElementById("access_token");

// get user hash
let userHash = document.cookie.split(";")[1].split("=")[1];

// set request options
let options = {
	method: 'POST',
	headers: {
	'Content-Type': 'application/json',
	},
	body: JSON.stringify({"user_hash": userHash})
};

// get user data
fetch("/api/user", options).then(data => {
	return data.json();
}).then(jsonObj => {
	console.log(jsonObj);
	firstName.value = jsonObj.first_name;
	lastName.value = jsonObj.last_name;
	email.value = jsonObj.email;
	phoneNum.value = jsonObj.phone_number;
	accessToken.value = jsonObj.access_token;
});