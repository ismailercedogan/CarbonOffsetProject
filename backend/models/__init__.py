from flask import Blueprint

main = Blueprint('models', __name__)

from app.main import routes
