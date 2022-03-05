const filesContainer = document.getElementById("files-container");

// set request options
let options = {
	method: 'POST',
	headers: {
	'Content-Type': 'application/json',
	},
	body: JSON.stringify({"user_uuid": "5d59daf3-f7cb-4a79-8c69-ec657aebb89a"})
};

// get user data
fetch("/api/v3/users", options).then(data => {
	return data.json();
}).then(jsonObj => {
	for (const key in jsonObj) {
		let node = document.createElement("h5");
		let textNode = document.createTextNode(jsonObj[key]);
		node.appendChild(textNode);
		node.classList.add("file-header");
		filesContainer.appendChild(node);
	}
});
