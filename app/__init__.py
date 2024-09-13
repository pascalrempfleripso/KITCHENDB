from flask import Flask
# from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+py{MYSQL_URL}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable to avoid warnings
#app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes
