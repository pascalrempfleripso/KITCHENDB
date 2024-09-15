# app/routes.py
from urllib.parse import urlsplit

import bcrypt
import sqlalchemy as sa
from flask import Response, flash, jsonify, make_response, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import app, db
from app.forms import LoginForm, RecipeForm, RegisterForm
from app.models import Ingredients, Instruction, Recipe, User, create_user


# Startseite / Index
@app.route("/")
@app.route("/index")
@login_required
def index() -> Response:
    # Ausgabe aller Rezepte:
    recipes = Recipe.query.all()
    return render_template("index.html", title="Home", recipes=recipes)


# User Login - Quelle https://blog.miguelgrinberg.com/
@app.route("/login", methods=["GET", "POST"])
def login() -> Response:
    if current_user.is_authenticated:
        return redirect(url_for("index"))
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


# User Logout - Quelle https://blog.miguelgrinberg.com/
@app.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("index"))


# Registrierung neuer User - Eigene Version mit Inspiration von https://blog.miguelgrinberg.com/
@app.route("/register", methods=["GET", "POST"])
def register() -> Response:
    form = RegisterForm()
    if form.validate_on_submit():
        create_user(form.username.data, form.email.data, form.password.data)
        flash(f"Congratulations {form.username.data}, you are now a registered User!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


# REST-API Funktionen
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


# Funktion zum Hinzufügen eines neuen Rezepts
@app.route("/add_recipe", methods=["GET", "POST"])
@login_required
def add_recipe() -> Response:
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(name=form.recipename.data, author_id=current_user.id)
        db.session.add(recipe)
        db.session.flush()  # Damit wird die recipe.id erstellt
        ingredients = Ingredients(recipe_id=recipe.id, name=form.ingredient1.data, amount=form.ingredient1_amount.data, unit=form.ingredient1_unit.data)
        db.session.add(ingredients)
        for task_form in form.tasks.data:
            task = Instruction(recipe_id=recipe.id, tasks=task_form.task.data)
            db.session.add(task)
        db.session.commit()
        return redirect(url_for("recipe_detail", recipe_id=recipe.id))
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{field.capitalize()}: {error}", "error")
    return render_template("add_recipe.html", form=form)


# Zusätzliche Seite zur Anzeige der Rezeptdetails
@app.route("/recipe/<int:recipe_id>")
@login_required
def recipe_detail(recipe_id: int) -> Response:
    # Query in DB "Recipe" anhand recipe_id
    recipe = Recipe.query.get_or_404(recipe_id)
    # Alle dazugehörigen Zutaten und Arbeitsschritte:
    ingredients = recipe.ingredients.all()
    instructions = recipe.instructions.all()
    # Aufruf .html
    return render_template("recipe_detail.html", recipe=recipe, ingredients=ingredients, instructions=instructions)


# Export eines Rezept in ein .txt File
@app.route("/recipe/<int:recipe_id>/export")
@login_required
def export_recipe(recipe_id: int) -> Response:
    # Query in DB "Recipe" anhand recipe_id
    recipe = Recipe.query.get_or_404(recipe_id)
    # Alle dazugehörigen Zutaten und Arbeitsschritte:
    ingredients = recipe.ingredients.all()
    instructions = recipe.instructions.all()
    # Inhalt für .txt file
    recipe_text = f"Rezept: {recipe.name}\n"
    recipe_text += f"Autor: {recipe.author.username}\n\n"
    recipe_text += "Zutaten:\n"
    for ingredient in ingredients:
        recipe_text += f"- {ingredient.amount} {ingredient.unit} {ingredient.name}\n"
    recipe_text += "\nAnleitung:\n"
    for idx, instruction in enumerate(instructions, start=1):
        recipe_text += f"{idx}. {instruction.tasks}\n"
    # Response mit .txt-File-Inhalt erstellen
    response = make_response(recipe_text)
    # Header für File-Download setzen
    response.headers["Content-Disposition"] = f"attachment; filename={recipe.name}.txt"
    response.headers["Content-Type"] = "text/plain"
    return response
