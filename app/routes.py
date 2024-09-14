# app/routes.py
from urllib.parse import urlsplit

import bcrypt
import sqlalchemy as sa
from flask import Response, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User, create_user


@app.route("/")
@app.route("/index")
@login_required
def index() -> Response:
    posts = [{"author": {"username": "Pascal"}, "body": "Offene Calzone"}]
    return render_template("index.html", title="Home", posts=posts)


# Login Form:
@app.route("/login", methods=["GET", "POST"])
def login() -> Response:
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not bcrypt.checkpw(form.password.data.encode(), user.password_hash.encode()):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


# Register Form:
@app.route("/register", methods=["GET", "POST"])
def register() -> Response:
    form = RegisterForm()
    if form.validate_on_submit():
        create_user(form.username.data, form.email.data, form.password.data)
        flash(f"Congratulations {form.username.data}, you are now a registered User!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


# REST users
# GET ALL USERS
@app.route("/users", methods=["GET"])
def get_users() -> Response:
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in User.query.all()])


# GET SPECIFIC USER
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> Response:
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email})


# POST/CREATE NEW USER USING REST-API
@app.route("/users", methods=["POST"])
def post_users() -> Response:
    data = request.get_json()
    create_user(username=data["username"], email=data["email"], password=data["password"])
    return jsonify({"message": "User created successfully"}), 201


# PATCH/MODIFY USER USING REST-API
@app.route("/users/<int:user_id>", methods=["PATCH"])
def patch_user(user_id: int) -> Response:
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email})
