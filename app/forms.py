from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, PasswordField, StringField, SubmitField, TextAreaField, ValidationError
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


# validator for metric units
def validate_metric_unit(form, field) -> None:
    valid_metric_units = ["g", "kg", "ml", "l", "mg"]
    if field.data not in valid_metric_units:
        msg = f"'{field.data}' is not a valid metric unit. Please use one of: {', '.join(valid_metric_units)}"
        raise ValidationError(msg)


class IngredientForm(FlaskForm):
    name = StringField("Ingredient Name", validators=[DataRequired(), Length(max=100)])
    amount = StringField("Amount", validators=[DataRequired()])
    unit = StringField("Unit", validators=[DataRequired(), Length(max=20), validate_metric_unit])


class InstructionForm(FlaskForm):
    task = TextAreaField("Instruction", validators=[DataRequired(), Length(max=5000)])


class RecipeForm(FlaskForm):
    name = StringField("Recipe Name", validators=[DataRequired(), Length(max=200)])
    author = StringField("Author Name", validators=[DataRequired(), Length(max=64)])

    # Ingredients: A list of ingredients
    ingredients = FieldList(FormField(IngredientForm), min_entries=1, max_entries=20)

    # Instructions: A list of instructions
    instructions = FieldList(FormField(InstructionForm), min_entries=1, max_entries=20)
    submit = SubmitField("Submit Recipe")
