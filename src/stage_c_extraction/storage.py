import json
from pathlib import Path
from typing import Optional
from .schema import ExtractedDataSchema
from pymongo import MongoClient
import config

class JSONStorage:
    def __init__(self, output_path: str = "extracted_data.json"):
        self.output_path = Path(output_path)
    
    def save(self, data: ExtractedDataSchema):
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(
                data.model_dump(mode='json'),
                f,
                ensure_ascii=False,
                indent=2,
                default=str
            )
        print(f"Saved extracted data to {self.output_path}")
    
    def load(self) -> Optional[ExtractedDataSchema]:
        if not self.output_path.exists():
            return None
        
        with open(self.output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return ExtractedDataSchema(**data)

class MongoDBStorage:
    def __init__(self):
        self.client = MongoClient(config.MONGODB_URI)
        self.db = self.client[config.MONGODB_DB_NAME]
        self.collection = self.db['extracted_items']
    
    def save(self, data: ExtractedDataSchema):
        self.collection.delete_many({})
        
        doc = data.model_dump(mode='json')
        self.collection.insert_one(doc)
        
        print(f"Saved extracted data to MongoDB: {config.MONGODB_DB_NAME}")
    
    def load(self) -> Optional[ExtractedDataSchema]:
        doc = self.collection.find_one()
        
        if not doc:
            return None
        
        doc.pop('_id', None)
        return ExtractedDataSchema(**doc)
    
    def query_decisions(self, tags: Optional[list] = None):
        data = self.load()
        if not data:
            return []
        
        decisions = data.items.decisions
        
        if tags:
            decisions = [d for d in decisions if any(tag in d.tags for tag in tags)]
        
        return decisions
    
    def query_rules(self, scope: Optional[str] = None):
        data = self.load()
        if not data:
            return []
        
        rules = data.items.rules
        
        if scope:
            rules = [r for r in rules if r.scope == scope]
        
        return rules
    
    def query_warnings(self, severity: Optional[str] = None):
        data = self.load()
        if not data:
            return []
        
        warnings = data.items.warnings
        
        if severity:
            warnings = [w for w in warnings if w.severity.value == severity]
        
        return warnings
