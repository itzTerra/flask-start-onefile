from flask import Flask, render_template, request, redirect, url_for, session
from db import SQLite
import functools
# from traceback import format_exc
# from werkzeug.security import generate_password_hash, check_password_hash
# from os import environ
# from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = b"totoj e zceLa n@@@hodny retezec nejlep os.urandom(24)"
# load_dotenv(".env")
# app.secret_key = environ.get("SECRET_KEY")


# Redirect decorator
def req_login(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper

# Render template with default data
def render_template_with_err(template: str, **data):
    base_error = ""
    if "error" in session:
        base_error = session.pop("error")

    return render_template(template, base_error=base_error, **data)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")



### Local testing - flask run from console preferred!
# if __name__ == "__main__":
#     # import os
#     # os.chdir("..")
#     app.run()