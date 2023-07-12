from flask import Flask
from config import Config
from flask_migrate import Migrate
from .models import db, User
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    #Return User.query.filter_by(id=user_id).first()
    return User.query.get(user_id)

login_manager.login_view='login'

from . import routes, models