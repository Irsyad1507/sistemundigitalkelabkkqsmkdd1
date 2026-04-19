from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from app.admin_routes import admin_bp
from app.calon_routes import calon_bp

app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(calon_bp, url_prefix="/calon")

from app import routes, models

app.jinja_env.globals.update(isinstance=isinstance, Admin=models.Admin)

# Will add logging support for production
