from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jqt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy import MetaData
from dotenv import load_dotenv
import os

# load .env
load_dotenv()

app = Flask(__name__)
CORS(app) # cross-origin requests (frontend can talk to backend)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turns off modification tracking which wastes memory

app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY") # not hard coding a secret key

app.json.compact = False #pretty json

# standardize naming foreign keys
metadata = MetaData(
  naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  }
)

db = SQLAlchemy(metadata=metadata) # creates the sqlalchemy object
db.init_app(app) # connects sqlalchemy to the flask app

# connects Flask-Migrate to the app and to the db
migrate = Migrate(app, db)

#initialize and create API
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)