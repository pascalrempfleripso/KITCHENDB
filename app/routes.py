# app/routes.py
import bcrypt
from flask import Response, flash, jsonify, redirect, render_template, request, url_for

from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User, create_user


@app.route("/")
@app.route("/index")
def index() -> Response:
    user = {"username": "Pascal"}
    posts = [{"author": {"username": "Pascal"}, "body": "Offene Calzone"}]
    return render_template("index.html", title="Home", user=user, posts=posts)


# Login Form:
@app.route("/login", methods=["GET", "POST"])
def login() -> Response:
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}")
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form)


# Register Form:
@app.route("/register", methods=["GET", "POST"])
def register() -> Response:
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f"Register requested for user {form.username.data}")
        create_user(form.username.data, form.email.data, form.password.data)
        return redirect(url_for("index"))
    return render_template("register.html", title="Sign In", form=form)


# REST users
@app.route("/users", methods=["GET"])
def get_users() -> Response:
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in User.query.all()])


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> Response:
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email})


@app.route("/users", methods=["POST"])
def post_users() -> Response:
    data = request.get_json()
    create_user(username=data["username"], email=data["email"], password=data["password"])
    return jsonify({"message": "User created successfully"}), 201


@app.route("/users/<int:user_id>", methods=["PATCH"])
def patch_user(user_id: int) -> Response:
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email})
