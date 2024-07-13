from flask import Flask
from app.LLM_module import blueprint as LLM_module
from config import Config
from app.extensions import LLM

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = app.config['SESSION_SECRET_KEY']

    # extensions
    LLM.init_app(app)

    @app.route('/')
    def home():
        return dict(mssg='Welcome to the Chatbot'), 200
    
    app.register_blueprint(LLM_module)
    
    return app