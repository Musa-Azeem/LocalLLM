from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http.exceptions import UnexpectedResponse
import uuid

class VectorDBWrapper:
    def __init__(self):
        self.client = None

    def init_app(self, app):
        self.app = app
        self.collection_name = app.config['COLLECTION_NAME']
        self.doc_collection_name = app.config['DOC_COLLECTION_NAME']
        self.client = QdrantClient(
            host=app.config['QDRANT_HOST'], 
            port=app.config['QDRANT_PORT'], 
        )
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=app.config['EMB_DIM'], 
                    distance=Distance.DOT
                )
            )
            print(f'Created Collection {self.collection_name}')
        except UnexpectedResponse as e:
            print(f'Collection {self.collection_name} already exists')
        try:
            self.client.create_collection(
                collection_name=self.doc_collection_name,
                vectors_config=VectorParams(
                    size=1,
                    distance=Distance.DOT # unused
                )
            )
            print(f'Created Collection {self.doc_collection_name}')
        except UnexpectedResponse as e:
            print(f'Collection {self.doc_collection_name} already exists')

    def search(self, vector, top_k=5):
        top_k = self.client.search(
            collection_name=self.collection_name, 
            query_vector=vector,
            limit=top_k
        )
        if len(top_k) == 0:
            return None
        return top_k
    
    def get_doc(self, doc_id):
        doc = self.client.retrieve(
            collection_name=self.doc_collection_name, 
            ids=[doc_id]
        )
        if len(doc) == 0:
            return None
        return doc[0]
    
    def insert_doc(self, entries, url):
        doc = '\n'.join(entries)
        doc_id = str(uuid.uuid4())
        self.client.upsert(
            collection_name=self.doc_collection_name,
            wait=True,
            points=[PointStruct(
                id=doc_id,
                vector=[0],
                payload={'text': doc, 'url': url}
            )]
        )
        return doc_id
    
    def insert_entries(self, entries, doc_embeddings, doc_id):
        points = [PointStruct(
            id=str(uuid.uuid4()), 
            vector=doc_embeddings[i],
            payload={
                'text': entries[i],
                'doc_id': doc_id
            }
        ) for i in range(len(entries))]

        self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=points,
        )