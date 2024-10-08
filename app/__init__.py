from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
# Variabeln für SQL
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Variabeln für Login
login = LoginManager()
login.init_app(app)
login.login_view = "login"

from app import routes, models  # noqa: E402, F401, I001
