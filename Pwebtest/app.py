import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
# from flask_mail import Mail, Message
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

#mail
# app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_DEFAULT_SENDER"]
# app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
# mail = Mail(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
# app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///Student.db")

@app.after_request
def after_request(response):
    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    try:
        tutors = db.execute("SELECT * FROM Hired WHERE id=?", user_id)
        empty=False
    except:
        empty=True
    return render_template("index.html",tutors=tutors, empty=empty)

@app.route("/regtutor" ,methods=["GET", "POST"])
@login_required
def reg():
    if request.method=="POST":
        email = request.form.get("email")
        name = request.form.get("username")
        password = request.form.get("password")
        # need to verify if it is the correct user TO DO
        subjects = request.form.get("subjects")
        timingW = request.form.get("timing")
        aboutU = request.form.get("AboutU")
        user_id = session["user_id"]

        #Gets the time when the offer is posted
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y %H:%M:%S")
        db.execute("INSERT INTO tutors(user_id,name,subject,email,timing,Aboutthem,Date) VALUES(?,?,?,?,?,?,?)",user_id,name,subjects,email,timingW,aboutU,date_str)
        return render_template("index.html")
    else:
        return render_template("regtutor.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["passhash"], request.form.get("password")):
            reply = "invalid username and/or password"
            return render_template("login.html", reply=reply)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    #Register user
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if username == "":
            reply = "Please enter a valid username" # DECISION : IS THIS A GOOD WAY OF GIVING ERRORS TO USER
            return render_template("register.html", reply=reply)
        if password == "" or confirmation == "" or password != confirmation:
            reply = "No password entered in one or both fields or password is not the same in both fields"
            return render_template("register.html", reply=reply)
        passhash = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users(username,passhash) VALUES(?,?)", username, passhash)
        except:
            reply = "Username already exists"
            return render_template("register.html", reply=reply)
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        return render_template("index.html")
    elif request.method == "GET":
        return render_template("register.html")

@app.route("/tutors")
@login_required
def tutor():
    tutors = db.execute("SELECT name, subject, email, timing, Aboutthem, Date FROM tutors ORDER BY Date ASC")
    return render_template("tutors.html", tutors=tutors)


@app.route("/hire", methods=["GET", "POST"])
@login_required
def hire():
    if request.method=="POST":
        # email = request.form.get("email")
        # name = request.form.get("name")
        # subjects = request.form.get("subjects")
        # timingW = request.form.get("timing")
        # aboutU = request.form.get("AboutU")
        # DateP = request.form.get("Date")
        # user_id = session["user_id"]
        # db.execute("INSERT INTO Hired(user_id,name,subject,email,timing,Aboutthem,Date) VALUES(?,?,?,?,?,?,?)",user_id,name,subjects,email,timingW,aboutU,DateP)
        # INCORRECT USE FIND CORRECT SOULTION
        # ---- TO DO ----
        return render_template("index.html")
    else:
        return render_template("tutor.html")