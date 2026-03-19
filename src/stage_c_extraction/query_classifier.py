from enum import Enum
from llama_index.llms.cohere import Cohere
from pydantic import BaseModel, Field
import config

class QueryType(str, Enum):
    SEMANTIC = "semantic"
    STRUCTURED_LIST = "structured_list"
    STRUCTURED_LATEST = "structured_latest"
    STRUCTURED_TIME_BASED = "structured_time_based"

class QueryClassification(BaseModel):
    query_type: QueryType = Field(description="The type of query")
    reasoning: str = Field(description="Why this classification was chosen")
    item_type: str = Field(default="", description="If structured, what item type (decisions, rules, warnings, etc.)")
    filters: dict = Field(default_factory=dict, description="Any filters to apply")

class QueryClassifier:
    def __init__(self):
        self.llm = Cohere(
            api_key=config.COHERE_API_KEY,
            model="command-r-plus"
        )
    
    def classify(self, query: str) -> QueryClassification:
        prompt = f"""
        Classify the following user query into one of these types:
        
        1. SEMANTIC - General questions that need semantic search across documents
           Examples: "How to install?", "What is the main color?", "Explain the architecture"
        
        2. STRUCTURED_LIST - Questions asking for a complete list of items
           Examples: "List all decisions", "Show all rules", "What are all the warnings?"
        
        3. STRUCTURED_LATEST - Questions asking for the most recent/current state
           Examples: "What's the current guideline for RTL?", "Latest decision about DB?"
        
        4. STRUCTURED_TIME_BASED - Questions with time constraints
           Examples: "What changed last week?", "Warnings from yesterday", "Recent decisions"
        
        User Query: "{query}"
        
        Classify this query and explain your reasoning.
        Also identify if it relates to: decisions, rules, warnings, dependencies, or changes.
        """
        
        response = self.llm.complete(prompt)
        response_text = str(response).lower()
        
        if "list" in query.lower() or "all" in query.lower() or "כל" in query:
            query_type = QueryType.STRUCTURED_LIST
            reasoning = "Query asks for a complete list"
        elif "latest" in query.lower() or "current" in query.lower() or "עדכני" in query or "נוכחי" in query:
            query_type = QueryType.STRUCTURED_LATEST
            reasoning = "Query asks for latest/current information"
        elif any(word in query.lower() for word in ["last week", "yesterday", "recent", "שבוע", "אתמול", "לאחרונה"]):
            query_type = QueryType.STRUCTURED_TIME_BASED
            reasoning = "Query has time-based constraints"
        else:
            query_type = QueryType.SEMANTIC
            reasoning = "General semantic query"
        
        item_type = ""
        if "decision" in query.lower() or "החלט" in query:
            item_type = "decisions"
        elif "rule" in query.lower() or "guideline" in query.lower() or "כלל" in query or "הנחי" in query:
            item_type = "rules"
        elif "warning" in query.lower() or "alert" in query.lower() or "אזהר" in query or "רגיש" in query:
            item_type = "warnings"
        elif "dependency" in query.lower() or "תלוי" in query:
            item_type = "dependencies"
        elif "change" in query.lower() or "שינוי" in query:
            item_type = "changes"
        
        return QueryClassification(
            query_type=query_type,
            reasoning=reasoning,
            item_type=item_type
        )
