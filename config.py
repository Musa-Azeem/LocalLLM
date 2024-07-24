from dotenv import load_dotenv
import os
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY')
    # assert SESSION_SECRET_KEY is not None, "SESSION_SECRET_KEY is not set. Did you forget to create a .env file?"
    SESSION_TIMEOUT = os.getenv('SESSION_TIMEOUT') or 60 * 60 * 24  # 24 hours
    REDIS_HOST = os.getenv('REDIS_HOST') or 'localhost'
    REDIS_PORT = os.getenv('REDIS_PORT') or 6379

    QDRANT_HOST = os.getenv('QDRANT_HOST') or 'localhost'
    QDRANT_PORT = os.getenv('QDRANT_PORT') or 6333

    MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR') or os.path.expanduser('~/.cache/huggingface/hub')
    # MODEL_NAME = os.getenv('MODEL_NAME') or 'QuantFactory/Meta-Llama-3-8B-Instruct-GGUF-v2'
    MODEL_NAME = os.getenv('MODEL_NAME') or 'QuantFactory/Meta-Llama-3.1-8B-Instruct-GGUF'
    # MODEL_GGUF_FILE = os.getenv('MODEL_GGUF_FILE') or 'Meta-Llama-3-8B-Instruct-v2.Q3_K_L.gguf'
    MODEL_GGUF_FILE = os.getenv('MODEL_GGUF_FILE') or 'Meta-Llama-3.1-8B-Instruct.Q4_K_M.gguf'

    EMB_MODEL_NAME = os.getenv('EMB_MODEL_NAME') or 'infgrad/stella_en_400M_v5'
    EMB_DIM = os.getenv('EMB_DIM') or 1024

    SYSTEM_MESSAGE = os.getenv('SYSTEM_MESSAGE') or (
        'Your name is Jarvis and you work at SIOS Technology Corp. You are an '
        'assistant that answers questions using information in a provided '
        'document. Prompts you receive will be formatted as follows:\n'
        'DOCUMENT:\n<document>\n'
        'USER QUESTION:\n<question>\n'
    )