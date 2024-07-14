from flask import Blueprint

blueprint = Blueprint('session_module', __name__)

from app.session_module import routes