from flask import Flask
from .models import db
from config import Config
from .routes import views
from .extension import mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

csrf=CSRFProtect()
def create_app():
    app=Flask(__name__,static_folder='static',static_url_path='/static')
    app.config.from_object(Config)
    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    migrate=Migrate(app,db)
    app.register_blueprint(views)
    return app
