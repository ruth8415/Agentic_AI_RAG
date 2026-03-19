from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

class EventType(Enum):
    QUERY_RECEIVED = "query_received"
    QUERY_VALIDATED = "query_validated"
    QUERY_INVALID = "query_invalid"
    RETRIEVAL_STARTED = "retrieval_started"
    RETRIEVAL_COMPLETED = "retrieval_completed"
    RETRIEVAL_FAILED = "retrieval_failed"
    LOW_CONFIDENCE = "low_confidence"
    SYNTHESIS_STARTED = "synthesis_started"
    SYNTHESIS_COMPLETED = "synthesis_completed"
    SYNTHESIS_FAILED = "synthesis_failed"
    RESPONSE_READY = "response_ready"
    ERROR_OCCURRED = "error_occurred"

@dataclass
class Event:
    type: EventType
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    
    def __str__(self):
        return f"Event({self.type.value}, data_keys={list(self.data.keys())})"

@dataclass
class WorkflowState:
    query: str = ""
    validated: bool = False
    retrieved_nodes: List[Any] = None
    confidence_score: float = 0.0
    needs_more_context: bool = False
    response: str = ""
    sources: List[Dict] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.retrieved_nodes is None:
            self.retrieved_nodes = []
        if self.sources is None:
            self.sources = []
