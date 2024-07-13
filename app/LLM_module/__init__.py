from flask import Blueprint

blueprint = Blueprint('LLM_module', __name__)

from app.LLM_module import routes