from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e556435e8b426aa01b45b8d52935e952'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# an Engine, which the Session will use for connection resources
engine = create_engine('sqlite:///climb.db')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

from pythontest import routes