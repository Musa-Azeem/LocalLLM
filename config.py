from dotenv import load_dotenv
import os
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY')
    assert SESSION_SECRET_KEY is not None, "SESSION_SECRET_KEY is not set. Did you forget to create a .env file?"

    MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR') or os.path.expanduser('~/.cache/huggingface/hub')
    MODEL_NAME = os.getenv('MODEL_NAME') or 'QuantFactory/Meta-Llama-3-8B-Instruct-GGUF-v2'
    MODEL_GGUF_FILE = os.getenv('MODEL_GGUF_FILE') or 'Meta-Llama-3-8B-Instruct-v2.Q3_K_L.gguf'