# app/routes.py
from flask import flash, jsonify, redirect, render_template, url_for

from app import app
from app.forms import LoginForm
from app.models import User


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Pascal"}
    posts = [{"author": {"username": "Pascal"}, "body": "Offene Calzone"}]
    return jsonify([{"id":user.username}for user in User.query.all()])
    return render_template("index.html", title="Home", user=user, posts=posts)


# Login Form:
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}"
        )
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)
