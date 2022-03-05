const registerForm = document.getElementById("register-form");
const firstName = document.getElementById("first-name");
const lastName = document.getElementById("last-name");
const email = document.getElementById("email");
const password = document.getElementById("password");


const getDate = () => {
	let today = new Date();
	let dd = String(today.getDate()).padStart(2, '0');
	let mm = String(today.getMonth() + 1).padStart(2, '0');
	let yyyy = today.getFullYear();
	return dd + mm + yyyy;
}

const genUserHash = (firstName, lastName) => {
	let fullName = firstName + lastName;
	let stringToHash = fullName.split("").reverse().join("") + getDate();
	let buffer = new TextEncoder("utf-8").encode(stringToHash);
	return crypto.subtle.digest("SHA-256", buffer).then(digest => {
		return hexEncodeData(digest);
	});
}

const hexEncodeData = digest => {
	// hex encode the SHA-256 raw bytes (buffer) equivalent to binascii.hexlify() in python
	let view = new DataView(digest);
	let hexEncodedHash = "";
	for (let i = 0; i < view.byteLength; i += 4) {
		let hexString = view.getUint32(i).toString(16);
		let padding = '00000000'
		let paddedHexString = (padding + hexString).slice(-padding.length)
		hexEncodedHash += paddedHexString;
	}
	return hexEncodedHash;
}

registerForm.addEventListener("submit", (e) => {
	e.preventDefault();
	genUserHash(firstName.value, lastName.value).then(userHash => {
		// send data to server
		let xhr = new XMLHttpRequest();
		xhr.open("POST", "/api/register", true);
		xhr.setRequestHeader('Content-Type', 'application/json');
		xhr.send(JSON.stringify({
			"first_name": firstName.value,
			"last_name": lastName.value,
			"email": email.value,
			"password": password.value,
			"user_hash": userHash
		}));

		xhr.onreadystatechange = () => {
			if (xhr.readyState === 4 && xhr.status === 200) {
				// redirect to the login page
				window.location.href = "/login";
			} else if (xhr.status === 409) {
				document.getElementById("email-registered").style.display = "block";
			}
		}
	});
});