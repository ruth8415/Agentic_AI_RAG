from typing import List
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Document
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import config
import ssl
import certifi
import os

os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

class DocumentIndexer:
    def __init__(self):
        self.embed_model = CohereEmbedding(
            api_key=config.COHERE_API_KEY,
            model_name="embed-multilingual-v3.0"
        )
        
        self.node_parser = SentenceSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        
        self._init_pinecone()
    
    def _init_pinecone(self):
        pc = Pinecone(api_key=config.PINECONE_API_KEY)
        
        index_name = config.PINECONE_INDEX_NAME
        
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=1024,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=config.PINECONE_ENVIRONMENT or "us-east-1"
                )
            )
            print(f"Created Pinecone index: {index_name}")
        
        pinecone_index = pc.Index(index_name)
        self.vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    
    def create_index(self, documents: List[Document]) -> VectorStoreIndex:
        nodes = self.node_parser.get_nodes_from_documents(documents)
        
        print(f"Created {len(nodes)} nodes from {len(documents)} documents")
        
        for node in nodes:
            if "tool" in node.metadata:
                node.metadata["tool_name"] = node.metadata["tool"]
            if "file_path" in node.metadata:
                node.metadata["file"] = node.metadata["file_path"]
        
        storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
        
        index = VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            embed_model=self.embed_model,
            show_progress=True
        )
        
        print(f"Index created and stored in Pinecone")
        return index
    
    def load_index(self) -> VectorStoreIndex:
        index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store,
            embed_model=self.embed_model
        )
        
        print("Index loaded from Pinecone")
        return index
