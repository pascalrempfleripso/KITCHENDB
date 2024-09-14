from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-Mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")


class IngredientForm(FlaskForm):
    name = StringField("Ingredient Name", validators=[DataRequired(), Length(max=100)])
    amount = StringField("Amount", validators=[DataRequired()])
    unit = SelectField(
        "Unit",
        choices=[
            ("mg", "milligrams (mg)"),
            ("g", "grams (g)"),
            ("kg", "kilograms (kg)"),
            ("ml", "milliliters (ml)"),
            ("l", "liters (l)"),
        ],
        validators=[DataRequired()],
    )


class InstructionForm(FlaskForm):
    task = TextAreaField("Instruction", validators=[DataRequired(), Length(max=5000)])


class RecipeForm(FlaskForm):
    name = StringField("Recipe Name", validators=[DataRequired(), Length(max=200)])
    author = StringField("Author Name", validators=[DataRequired(), Length(max=64)])
    ingredients = StringField("Ingredient Name", validators=[DataRequired(), Length(max=100)])
    instructions = TextAreaField("Instruction", validators=[DataRequired(), Length(max=5000)])
    submit = SubmitField("Submit Recipe")
