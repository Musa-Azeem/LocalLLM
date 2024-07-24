from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.exceptions import UnexpectedResponse

DOC_COLLECTION_NAME = "context_docs"
COLLECTION_NAME = "vector_entries"

class VectorDBWrapper:
    def __init__(self):
        self.client = None

    def init_app(self, app):
        self.app = app
        self.client = QdrantClient(
            host=app.config['QDRANT_HOST'], 
            port=app.config['QDRANT_PORT'], 
        )
        try:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=app.config['EMB_DIM'], 
                    distance=Distance.DOT
                ),
            )
            print(f'Created Collection {COLLECTION_NAME}')
        except UnexpectedResponse as e:
            print(f'Collection {COLLECTION_NAME} already exists')

    def search(self, vector, top_k=5):
        return self.client.search(
            collection_name=COLLECTION_NAME, 
            query_vector=vector,
            limit=top_k
        )
    
    def get_doc(self, doc_id):
        doc = self.client.retrieve(
            collection_name=DOC_COLLECTION_NAME, 
            ids=[doc_id]
        )
        if len(doc) == 0:
            return None
        return doc[0]