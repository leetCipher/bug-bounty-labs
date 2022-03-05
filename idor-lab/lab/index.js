const express = require("express");
const exphbs = require('express-handlebars');
const mysqlDB = require("./db.js");
const path = require("path");
const app = express();
const apiRouter = require("./routes/api.js");
const port = 3000;

// handlebars options
app.engine('handlebars', exphbs());
app.set('view engine', 'handlebars');

// make express handle json data and url encoded data
app.use(express.json());
app.use(express.urlencoded({extended: true}));

// tell express where to look for js and css files
app.use(express.static(path.join(__dirname, "assets")))

// route all API calls to the api-router (routes/api.js)
app.use("/api", apiRouter);

// check if auth cookie is set
const checkAuthCookie = (cookies) => {
    // check if auth cookie is already set
    if (cookies !== undefined) {
        let cookiesArray = cookies.split(";");
        for (let cookie of cookiesArray) {
            if (cookie.split("=")[0] === "auth" && cookie.split("=")[1].length === 64) {
                return true;
            } else {
                return false;
            }
        }
    } else {
        return false;
    }
}

app.get('/', (req, res) => {
    // check if auth cookie is already set
    if (!checkAuthCookie(req.headers.cookie)) {
        res.redirect("/login");
    } else {
        res.render("home");
    }
});

app.get("/profile", (req, res) => {
    // check if auth cookie is already set
    if (!checkAuthCookie(req.headers.cookie)) {
        res.redirect("/login");
    } else {
        res.render("profile");
    }
});

app.get("/login", (req, res) => {
    // check if auth cookie is already set
    if (checkAuthCookie(req.headers.cookie)) {
        res.redirect("/");
    } else {
        res.render("login");
    }
});

app.get("/logout", (req, res) => {
    // destroy the auth cookie and redirect to login page
    res.cookie("auth", {expires: new Date(0)});
    res.cookie("user_hash", {expires: new Date(0)});
    res.redirect("/login");
});

app.get("/register", (req, res) => {
    // check if auth cookie is already set
    if (checkAuthCookie(req.headers.cookie)) {
        res.redirect("/");
    } else {
        res.render("register");
    }
});

// connect to MySQL
mysqlDB.connect(err => {
    if (err) throw err;
    console.log("MySQL connected...");
});

app.listen(port, () => {
    console.log(`app is running on port ${port}`)
});