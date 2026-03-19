from typing import Dict, List
from .query_classifier import QueryClassifier, QueryType
from .storage import JSONStorage, MongoDBStorage
from llama_index.llms.cohere import Cohere
import config

class HybridQueryRouter:
    def __init__(self, semantic_query_engine, storage_type: str = "json"):
        self.semantic_query_engine = semantic_query_engine
        self.classifier = QueryClassifier()
        
        if storage_type == "mongodb":
            self.storage = MongoDBStorage()
        else:
            self.storage = JSONStorage()
        
        self.llm = Cohere(
            api_key=config.COHERE_API_KEY,
            model="command-r-plus"
        )
    
    def route_query(self, query: str) -> Dict:
        classification = self.classifier.classify(query)
        
        print(f"Query classified as: {classification.query_type.value}")
        print(f"Reasoning: {classification.reasoning}")
        
        if classification.query_type == QueryType.SEMANTIC:
            return self._handle_semantic_query(query)
        else:
            return self._handle_structured_query(query, classification)
    
    def _handle_semantic_query(self, query: str) -> Dict:
        result = self.semantic_query_engine.query(query)
        
        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "query_type": "semantic",
            "confidence": result.get("confidence", 0)
        }
    
    def _handle_structured_query(self, query: str, classification) -> Dict:
        data = self.storage.load()
        
        if not data:
            return {
                "answer": "לא נמצא מידע מובנה. יש להריץ תהליך חילוץ נתונים תחילה.",
                "sources": [],
                "query_type": "structured",
                "error": "no_extracted_data"
            }
        
        items = []
        
        if classification.item_type == "decisions":
            items = data.items.decisions
        elif classification.item_type == "rules":
            items = data.items.rules
        elif classification.item_type == "warnings":
            items = data.items.warnings
        elif classification.item_type == "dependencies":
            items = data.items.dependencies
        elif classification.item_type == "changes":
            items = data.items.changes
        else:
            items = (
                data.items.decisions +
                data.items.rules +
                data.items.warnings +
                data.items.dependencies +
                data.items.changes
            )
        
        if classification.query_type == QueryType.STRUCTURED_LATEST:
            items = sorted(items, key=lambda x: x.observed_at, reverse=True)[:5]
        elif classification.query_type == QueryType.STRUCTURED_TIME_BASED:
            from datetime import datetime, timedelta
            week_ago = datetime.now() - timedelta(days=7)
            items = [item for item in items if item.observed_at >= week_ago]
        
        items_text = self._format_items(items)
        
        synthesis_prompt = f"""
        Based on the following structured data, answer the user's question.
        
        User Question: {query}
        
        Data:
        {items_text}
        
        Provide a clear and concise answer in Hebrew.
        """
        
        response = self.llm.complete(synthesis_prompt)
        answer = str(response)
        
        sources = []
        for item in items[:5]:
            sources.append({
                "type": classification.item_type,
                "content": str(item),
                "source": item.source.model_dump()
            })
        
        return {
            "answer": answer,
            "sources": sources,
            "query_type": "structured",
            "item_count": len(items)
        }
    
    def _format_items(self, items: List) -> str:
        if not items:
            return "No items found."
        
        formatted = []
        for i, item in enumerate(items[:20], 1):
            formatted.append(f"{i}. {item.model_dump_json(indent=2)}")
        
        return "\n\n".join(formatted)
