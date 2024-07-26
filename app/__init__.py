from flask import Flask
from app.LLM_module import blueprint as LLM_module
from app.embedding_module import blueprint as embedding_module
from app.session_module import blueprint as session_module
from config import Config
from app.extensions import LLM, redis_client, embedding_model, vector_db_client
import nltk
nltk.download('punkt')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # extensions
    redis_client.init_app(app)
    try:
        redis_client.ping()
    except:
        raise Exception('Redis connection failed')
    vector_db_client.init_app(app)
    LLM.init_app(app)
    embedding_model.init_app(app)

    @app.route('/')
    def home():
        return dict(mssg='Welcome to the Chatbot'), 200
    
    app.register_blueprint(LLM_module)
    app.register_blueprint(session_module)
    app.register_blueprint(embedding_module)
    
    return app