from flask import Flask
from .models import db
from config import Config
from .routes import views
from .extension import mail

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    app.register_blueprint(views)
    return app
