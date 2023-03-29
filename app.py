from flask import Flask, render_template, request, redirect, url_for, session
import functools
from db import MySQL # / SQLite
# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b"totoj e zceLa n@@@hodny retezec nejlep os.urandom(24)"


def req_login(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("base.html")

