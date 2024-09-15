# app.forms.py
from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


# Login Formular - Quelle https://blog.miguelgrinberg.com/
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


# Register Formular - Quelle https://blog.miguelgrinberg.com/
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-Mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Password wiederholen", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Registrieren")


# Sub-Formular zum Hinzufügen von Arbeitsschritten für Rezepte
class TaskForm(FlaskForm):
    task = StringField("Arbeitsschritt", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("csrf_enabled", False)  # Disable CSRF for this form
        super().__init__(*args, **kwargs)


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
    tasks = FieldList(FormField(TaskForm), min_entries=1)
    submit = SubmitField("Speichern")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("csrf_enabled", False)  # Disable CSRF for this form
        super().__init__(*args, **kwargs)
