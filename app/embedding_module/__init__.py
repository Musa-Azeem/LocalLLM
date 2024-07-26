from flask import Blueprint

blueprint = Blueprint('embedding_module', __name__)

from app.embedding_module import routes