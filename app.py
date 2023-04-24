from flask import Flask, render_template, request, redirect, url_for, session
from db import SQLite
import functools
from traceback import format_exc
from werkzeug.security import generate_password_hash, check_password_hash
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


@app.route('/register/', methods=('GET', 'POST'))
def register():
    error = ""
    success = ""
    
    if request.method == 'POST':
        try:
            username = request.form['username']
            pass1 = request.form['pass1']
            pass2 = request.form['pass2']

            if len(username) < 4 or len(username) > 15 or not username.isalnum():
                error = 'Wrong username.'
            elif len(pass1) < 5:
                error = 'Password too short.'
            elif pass1 != pass2:
                error = "Passwords do not match."
            else:
                with SQLite() as cur:
                    cur.execute("SELECT * FROM user WHERE username=?", (username,))

                    if cur.fetchone() is not None:
                        error = "Username already exists."
                    else:
                        cur.execute(
                            "INSERT INTO user (username, password) VALUES (?, ?)",
                            (username, generate_password_hash(pass1)),
                        )
                        cur.execute("COMMIT")
                        success = "User succesfully registered."

        except:
            print(format_exc())
            session["error"] = "Unknown error occured."
    
    session["last_url"] = url_for("register")
    return render_template_with_err('register.html', error=error, success=success)


@app.route('/login/', methods=('GET', 'POST'))
def login():
    if "user" in session:
        session.pop("user")
        return redirect(session.get("last_url", url_for("index")))
    
    error = ""
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['pass']
            
            with SQLite() as cur:
                cur.execute('SELECT * FROM user WHERE username=?', (username,))
                user = cur.fetchone()

                if user is None:
                    error = 'Incorrect username.'
                elif not check_password_hash(user[2], password):
                    error = 'Incorrect password.'
                else:
                    session["user"] = (user[1], user[3])
                    return redirect(session.get("last_url", url_for("index")))

        except:
            print(format_exc())
            session["error"] = "Unknown error occured."
    
    return render_template_with_err('login.html', error=error)


### Local testing - flask run from console preferred!
# if __name__ == "__main__":
#     # import os
#     # os.chdir("..")
#     app.run()