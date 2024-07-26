from sentence_transformers import SentenceTransformer
from huggingface_hub import hf_hub_download
from pathlib import Path

class EmbeddingWrapper:
    def __init__(self):
        self.app = None
        self.cache_dir = None
        self.model_name = None
        self.emb_dim = None
        self.model = None
        self.device = None
    
    def init_app(self, app):
        self.app = app
        self.cache_dir = Path(app.config['MODEL_CACHE_DIR'])
        self.model_name = app.config['EMB_MODEL_NAME']
        self.emb_dim = app.config['EMB_DIM']
        self.device = app.config['EMB_DEVICE']

        if not Path(self.cache_dir / f'models--{self.model_name.replace("/","--")}').exists():
            print(f'Downloading {self.model_name} from Hugging Face Hub...')
        else:
            print(f'Loading cached model: {self.model_name}...')

        self.model = SentenceTransformer(
            self.model_name, 
            trust_remote_code=True,
            device=self.device
        )
    
    def encode_query(self, sentences):
        prompt_name = "s2p_query" # Instruct: Given a web search query, retrieve relevant passages that answer the query.\nQuery: {query}
        # prompt_name = "s2s_query" # Instruct: Retrieve semantically similar text.\nQuery: {query}
        return self.model.encode(sentences, prompt_name=prompt_name, device=self.device)
    
    def encode_entries(self, entries):
        doc_embeddings = self.model.encode(entries, device=self.device)
        return doc_embeddings