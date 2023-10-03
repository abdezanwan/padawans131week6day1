from flask import Flask
from config import Config
from .models import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

from . import routes

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'  
login_manager.init_app(app)  

from .models import User  
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))