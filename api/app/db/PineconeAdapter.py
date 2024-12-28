
import os
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import time

class PineconeAdapter:
    def __init__(self, index_name='example-index', namespace='example-namespace'):
        load_dotenv()
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = index_name
        self.namespace = namespace

    def create_index(self):
        if not self.pc.has_index(self.index_name):
            self.pc.create_index(
                name=self.index_name,
                dimension=1024,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
            while not self.pc.describe_index(self.index_name).status['ready']:
                time.sleep(1)

    def get_index(self):
        return self.pc.Index(self.index_name)

    def embed_texts(self, texts, model='multilingual-e5-large', input_type='passage', truncate='END'):
        return self.pc.inference.embed(
            model=model,
            inputs=texts,
            parameters={'input_type': input_type, 'truncate': truncate}
        )

    def upsert_data(self, data):
        embeddings = self.embed_texts([d['text'] for d in data])
        records = [{'id': d['id'], 'values': e['values'], 'metadata': {'text': d['text']}} for d, e in zip(data, embeddings)]
        index = self.get_index()
        index.upsert(vectors=records, namespace=self.namespace)
        time.sleep(10)

    def query_index(self, query, top_k=3, model='multilingual-e5-large'):
        query_embedding = self.embed_texts([query], model=model, input_type='query')[0]
        index = self.get_index()
        return index.query(
            namespace=self.namespace,
            vector=query_embedding['values'],
            top_k=top_k,
            include_values=False,
            include_metadata=True
        )

    def get_index_stats(self):
        return self.get_index().describe_index_stats()
