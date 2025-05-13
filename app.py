import os
import re
import sqlite3
import sys

from datetime import datetime, timezone
from flask_session import Session
from flask import Flask, flash, redirect, render_template, url_for, request, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from random import shuffle

from helpers import apology, login_required, is_valid_email, is_valid_username, crop_to_aspect

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DATABASE = './guide.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    cur = get_db().cursor()
    # cur.execute("INSERT INTO sights (name, address, mark, categories, photos) VALUES (?, ?, ?, ?, ?)",
    #             ("Wyndham Grand", 
    #              "Stare Miasto, Floriańska 28", 
    #              4.7, 
    #              "Hotels", 
    #              "./static/wyndham.jpg")
    # )
    # cur.execute("INSERT INTO sights (name, address, mark, categories, photos) VALUES (?, ?, ?, ?, ?)",
    #             ("Muzeum Lotnictwa Polskiego", 
    #              "Czyżyny, Jana Pawłą II 39", 
    #              4.7, 
    #              "Museums", 
    #              "./static/muzeumlotnictwakrakow.jpg")
    # )
    # cur.execute("UPDATE sights SET photos = ? WHERE sight_id = 6", ('./static/andrzej.jpg',))
    sights = cur.execute("SELECT * FROM sights").fetchall()
    # get_db().commit() # Remember to commit the transaction after executing INSERT.
    for sight in sights:
    # get_db(). close()
        if os.path.isfile('./static/sights/' + str(sight[0]) + '.jpg'):
            continue
        if sight[0]:
            output = "./static/sights/" + str(sight[0]) + ".jpg"

            crop_to_aspect(sight[5], output, 5/4)

    sights_id = []
    try:
        rows = query_db("SELECT sight_id FROM favourites WHERE user_id = ?", (session["user_id"],))
        for row in rows:
            sights_id.append(int(row[0]))
    except:
        sights_id = []
    return render_template("index.html", sights=sights, favourites=sights_id)


@app.route("/login", methods=["POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = query_db("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0][3], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]
        # Redirect user to home page
        return redirect("/")
    

@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/profile")
@login_required
def profile():
    """Show user profile"""
    user = query_db("SELECT id, username, email FROM users WHERE id = ?", (session["user_id"],))
    if user == []:
        return apology("Looks like you don't have permission", 400)

    favourites = query_db("SELECT sight_id FROM favourites WHERE user_id = ?", 
                 (session["user_id"],))
    list = []
    if favourites == []:
        sights = []
    else:
        for favourite in favourites:
            list.append(int(favourite[0]))
    sights = query_db("SELECT * FROM sights WHERE sight_id IN (SELECT sight_id FROM favourites WHERE user_id = ?)", 
             (session["user_id"],))
    return render_template("profile.html", user=user[0], sights=sights, favourites=list)


@app.route("/favourite", methods=["POST"])
def favourite():
    """Add location to favourites"""  
    try:
        session["user_id"]
    except:
        return redirect("/register")
    element = request.form.get("index")
    rows = query_db("SELECT sight_id FROM favourites WHERE user_id = ?", (session["user_id"],))
    sights_id = []
    for row in rows:
        sights_id.append(int(row[0]))
    cur = get_db().cursor()
    if not rows or not int(element) in sights_id:
        cur.execute("INSERT INTO favourites (user_id, sight_id) VALUES (?, ?)",
                   (session["user_id"], request.form.get("index")))
    else:
        cur.execute("DELETE FROM favourites WHERE user_id = ? AND sight_id = ?",
                   (session["user_id"], request.form.get("index")))
    get_db().commit()
    get_db().close()
    return redirect(request.referrer)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{}|;:'\",.<>?/])[A-Za-z\d!@#$%^&*()_\-+=\[\]{}|;:'\",.<>?/]{8,}$"
        # Ensure email was correct
        if not is_valid_email(request.form.get("email")):
            return apology("email was invalid", 400)
        # Ensure username was correct
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not is_valid_username(request.form.get("username")):
            return apology("username must contain only latin letters, numbers, or '_' and be at least 4 symbols", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not re.match(pattern, request.form.get("password"), re.VERBOSE):
            # Check if password contains at least one uppercase letter, one lowercase letter, one digit, and one special character
            return apology("password must be contain at least one uppercase letter, one lowercase letter, one digit, and one special character", 403)
        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must repeat password", 400)
        # Ensure password and confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Ensure username is unique
        rows = query_db("SELECT username FROM users WHERE username = ?", (request.form.get("username"),))
        if len(rows) != 0:
            return apology("username already taken", 400)
        # Ensure email is unique
        emails = query_db("SELECT email FROM users WHERE email = ?", (request.form.get("email"),))
        if len(emails) != 0:
            return apology("email already taken", 400)
        # Hash the password
        hash = generate_password_hash(request.form.get("password"))

        # Insert new user into database
        cur = get_db().cursor()
        cur.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)",
            (request.form.get("username"),
             request.form.get("email"),
             hash,
            )
        )
        username = request.form.get("username")
        get_db().commit()
        get_db().close()
        # token = generate_token(request.form.get("email"))
        return redirect("/")
    else:
        return render_template("register.html")
    

@app.route("/change", methods=["POST"])
@login_required
def change():
    """Change password"""

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{}|;:'\",.<>?/])[A-Za-z\d!@#$%^&*()_\-+=\[\]{}|;:'\",.<>?/]{8,}$"
    # Ensure password was submitted
    if not request.form.get("password"):
        return apology("must provide new password", 400)
    # Check if password contains at least one uppercase letter, one lowercase letter, one digit, and one special character
    elif not re.match(pattern, request.form.get("password"), re.VERBOSE):
        return apology("password must be contain at least 8 symbols and among them: one uppercase letter, one lowercase letter, one digit, and one special character", 400)
    # Ensure confirmation was submitted
    elif not request.form.get("confirmation"):
        return apology("must repeat new password", 400)
    # Ensure password and confirmation match
    elif request.form.get("password") != request.form.get("confirmation"):
        return apology("passwords must match", 400)

    # Hash the password
    hash = generate_password_hash(request.form.get("password"))

    # Update password in db
    cur = get_db().cursor()
    cur.execute("UPDATE users SET hash = ? WHERE id = ?",
                (hash,
                session["user_id"],)
    )
    get_db().commit() # Remember to commit the transaction after executing INSERT.
    get_db().close()
    return redirect("/")


@app.route("/changeUsername", methods=["POST"])
@login_required
def changeUsername():
    """Change username"""

    # Ensure username was correct
    if not request.form.get("username"):
        return apology("must provide username", 400)
    elif not is_valid_username(request.form.get("username")):
        return apology("username must contain only latin letters, numbers, or '_' and be at least 4 symbols", 400)

    # Ensure username is unique
    rows = query_db("SELECT username FROM users WHERE username = ?", (request.form.get("username"),))
    if len(rows) != 0:
        return apology("username already taken", 400)

    # Update username in db
    cur = get_db().cursor()
    cur.execute("UPDATE users SET username = ? WHERE id = ?",
                (request.form.get("username"), 
                 session["user_id"],)
    )
    get_db().commit() # Remember to commit the transaction after executing INSERT.
    get_db().close()
    return redirect("/")


@app.route("/changeEmail", methods=["POST"])
@login_required
def changeEmail():
    """Change email"""
    # Ensure email was correct
    if not is_valid_email(request.form.get("email")):
        return apology("email was invalid", 400)
    # Ensure confirmation was submitted
    elif not request.form.get("confirmation"):
        return apology("must repeat new email", 400)
    # Ensure email and confirmation match
    elif request.form.get("email") != request.form.get("confirmation"):
        return apology("emails must match", 400)
    
    # Ensure email is unique
    emails = query_db("SELECT email FROM users WHERE email = ?", (request.form.get("email"),))
    if len(emails) != 0:
        return apology("email already taken", 400)

    # Update username in db
    cur = get_db().cursor()
    cur.execute("UPDATE users SET email = ? WHERE id = ?",
                (request.form.get("email"),
                 session["user_id"],)
    )
    get_db().commit() # Remember to commit the transaction after executing INSERT.
    get_db().close()
    return redirect("/")


@app.route("/card", methods=["POST"])
def card():
    """Show card page"""
    place = query_db("SELECT * FROM sights WHERE sight_id = ?", (request.form.get("sight"),))[0]
    if place[0] != 1:
            output = "./static/sights/" + str(place[0]) + "A.jpg"
            crop_to_aspect(place[5], output, 16/9)
    sights = query_db("SELECT * FROM sights WHERE mark > 4.7")
    shuffle(sights)

    sights_id = []
    try:
        rows = query_db("SELECT sight_id FROM favourites WHERE user_id = ?", (session["user_id"],))
        for row in rows:
            sights_id.append(int(row[0]))
    except:
        sights_id = [] 
    return render_template("article.html", place=place, sights=sights, favourites=sights_id)


@app.route("/category/<name>")
def category(name):
    """Show choosed category"""
    sights_id = []
    try:
        rows = query_db("SELECT sight_id FROM favourites WHERE user_id = ?", (session["user_id"],))
        for row in rows:
            sights_id.append(int(row[0]))
    except:
        sights_id = [] 

    if name == 'all-places':
        fullname = 'All places'
        sights = query_db("SELECT * FROM sights")
        return render_template("category.html", sights=sights, name=fullname, favourites=sights_id)
    
    fullname = query_db("SELECT fullname FROM categories WHERE name = ?", (name,))[0][0]
    sights = query_db("SELECT * FROM sights WHERE categories LIKE ?", ('%' + fullname + '%',))
    return render_template("category.html", sights=sights, name=fullname, favourites=sights_id)

