from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.llms.cohere import Cohere
import config

class RAGQueryEngine:
    def __init__(self, index: VectorStoreIndex, top_k: int = 5):
        self.index = index
        self.top_k = top_k
        
        self.llm = Cohere(
            api_key=config.COHERE_API_KEY,
            model="command-r-plus"
        )
        
        self.retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=self.top_k
        )
        
        self.response_synthesizer = get_response_synthesizer(
            llm=self.llm,
            response_mode="compact"
        )
        
        self.query_engine = RetrieverQueryEngine(
            retriever=self.retriever,
            response_synthesizer=self.response_synthesizer
        )
    
    def query(self, question: str) -> dict:
        response = self.query_engine.query(question)
        
        sources = []
        if hasattr(response, 'source_nodes'):
            for node in response.source_nodes:
                source_info = {
                    "text": node.node.text[:200] + "...",
                    "score": node.score,
                    "metadata": node.node.metadata
                }
                sources.append(source_info)
        
        return {
            "answer": str(response),
            "sources": sources
        }
