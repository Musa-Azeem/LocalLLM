from dotenv import load_dotenv
import os
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SESSION_TIMEOUT = float(os.getenv('SESSION_TIMEOUT', 60 * 60 * 24))  # 24 hours
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost') 
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)

    QDRANT_HOST = os.getenv('QDRANT_HOST', 'localhost')
    QDRANT_PORT = os.getenv('QDRANT_PORT', 6333)
    DOC_COLLECTION_NAME = os.getenv('DOC_COLLECTION_NAME', 'context_docs')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'vector_entries')
    SEARCH_TOP_K = int(os.getenv('SEARCH_TOP_K', 5))

    MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR', os.path.expanduser('~/.cache/huggingface/hub'))
    MODEL_NAME = os.getenv('MODEL_NAME', 'QuantFactory/Meta-Llama-3.1-8B-Instruct-GGUF')
    MODEL_GGUF_FILE = os.getenv('MODEL_GGUF_FILE', 'Meta-Llama-3.1-8B-Instruct.Q4_K_M.gguf')
    MODEL_N_CTX = int(os.getenv('MODEL_N_CTX', 2048))
    MODEL_MAX_TOKENS = int(os.getenv('MODEL_MAX_TOKENS', 512))
    MODEL_N_GPU_LAYERS = int(os.getenv('MODEL_N_GPU_LAYERS', 0))

    EMB_MODEL_NAME = os.getenv('EMB_MODEL_NAME', 'infgrad/stella_en_400M_v5')
    EMB_DIM = int(os.getenv('EMB_DIM', 1024))
    EMB_DEVICE = os.getenv('EMB_DEVICE', 'cuda')

    SYSTEM_MESSAGE = os.getenv('SYSTEM_MESSAGE', (
        'You work at SIOS Technology Corp. '
        'You are an assistant that answers questions using information in a '
        'provided document. Prompts you receive will be formatted as follows:\n'
        'DOCUMENT:\n<document>\n'
        'USER QUESTION:\n<question>\n'
    ))