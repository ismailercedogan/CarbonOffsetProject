import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.config.from_object(os.environ['APP_SETTINGS'])
            
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api')
    
    from app.debug import debug as debug_blueprint  # Add this line
    app.register_blueprint(debug_blueprint, url_prefix='/debug')  # Add this line

    return app
