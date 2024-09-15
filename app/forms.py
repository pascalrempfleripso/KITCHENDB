from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


# Login Formular - Quelle https://blog.miguelgrinberg.com/
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


# Register Formular - Quelle https://blog.miguelgrinberg.com/
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-Mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")


# Formular für das Hinzufügen neuer Rezepte
class RecipeForm(FlaskForm):
    recipename = StringField("Rezept", validators=[DataRequired()])
    ingredient1 = StringField("1. Zutat", validators=[DataRequired()])
    ingredient1_amount = IntegerField("1. Zutat Menge", validators=[DataRequired()])
    ingredient1_unit = SelectField(
        "Masseinheit",
        choices=[
            ("mg", "mg"),
            ("g", "g"),
            ("kg", "kg"),
            ("ml", "ml"),
            ("l", "l"),
            ("stk", "stk"),
        ],
        validators=[DataRequired()],
    )
    task1 = StringField("1. Arbeitsschritt", validators=[DataRequired()])
    submit = SubmitField("Speichern")
