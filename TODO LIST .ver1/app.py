import sqlite3
from typing import ItemsView
from flask import Flask, render_template, request, redirect
from flask_session import Session

app = Flask(__name__)
db = sqlite3.connect('user.db', check_same_thread=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            return render_template("error.html", message="Missing Name")

        password = request.form.get("password")
        if not password:
            return render_template("error.html", message="Missing Password")

        db.execute("INSERT INTO users (name, password) VALUES(?, ?)",
                   (name, password))
        db.commit()

        return render_template("success.html", message="You are Registerd")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        users = db.execute(
            "SELECT * FROM users WHERE name = (?) AND password = (?)", (name, password)).fetchmany()
        # rows[0][2] means select the password columns in the rows
        # because there only 1 username so len(rows) must be 1 & index will 0
        if len(users) != 1:
            return render_template("error.html", message="Invalid")
        else:
            return redirect("/todo")

    else:
        return render_template("login.html")


@app.route("/todo", methods=["POST", "GET"])
def todo():
    if request.method == "POST":
        items = request.form.get("todo")
        db.execute("INSERT INTO items (name) VALUES (?)", [items])

    ITEMS = db.execute(
        "SELECT DISTINCT name FROM items ORDER BY name").fetchall()
    return render_template("todo.html", item=ITEMS)


app.run()
