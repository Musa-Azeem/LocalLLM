from llama_cpp import Llama
from huggingface_hub import hf_hub_download
from pathlib import Path

class LLMWrapper:
    def __init__(self):
        pass

    def init_app(self, app):
        self.app = app
        self.cache_dir = Path(app.config['MODEL_CACHE_DIR'])
        self.model_name = app.config['MODEL_NAME']
        self.model_gguf_file = app.config['MODEL_GGUF_FILE']
        if not Path(self.cache_dir / f'models--{self.model_name.replace("/","--")}').exists():
            print(f'Downloading {self.model_name}/{self.model_gguf_file} from Hugging Face Hub...')
            hf_hub_download(self.model_name, cache_dir=self.cache_dir)
        else:
            print(f'Loading cached model: {self.model_name}/{self.model_gguf_file}...')

        self.model = Llama.from_pretrained(
            repo_id=self.model_name,
            filename=self.model_gguf_file,
            verbose=False,
            n_gpu_layers=-1,
            chat_template="llama3",
            cache_dir=self.cache_dir,
        )
    
    def create_chat_completion(self, messages):
        return self.model.create_chat_completion(messages, max_tokens=150)