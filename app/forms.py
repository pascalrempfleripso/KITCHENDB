from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
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


class RecipeForm(FlaskForm):
    recipename = StringField("Recipe", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    ingredient1 = StringField("1.Ingredient", validators=[DataRequired()])
    ingredient1_amount = IntegerField("1.Ingredient Amount", validators=[DataRequired()])
    ingredient1_unit = SelectField(
        "Unit",
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
    ingredient2 = StringField("2.Ingredient")
    ingredient2_amount = IntegerField("2.Ingredient Amount")
    ingredient3 = StringField("3.Ingredient")
    ingredient3_amount = IntegerField("3.Ingredient Amount")
    ingredient4 = StringField("4.Ingredient")
    ingredient4_amount = IntegerField("4.Ingredient Amount")
    ingredient5 = StringField("5.Ingredient")
    ingredient5_amount = IntegerField("5.Ingredient Amount")
    task1 = StringField("1. Task", validators=[DataRequired()])
    task2 = StringField("2. Task")
    task3 = StringField("3. Task")
    task4 = StringField("4. Task")
    task5 = StringField("5. Task")
    submit = SubmitField("Save")
