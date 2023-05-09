from flask import Flask, render_template, request, redirect, url_for, session
from db import SQLite
# import functools
from traceback import format_exc
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b"totoj e zceLa n@@@hodny retezec nejlep os.urandom(24)"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")



### Local testing - flask run from console preferred!
# if __name__ == "__main__":
#     # import os
#     # os.chdir("..")
#     app.run()