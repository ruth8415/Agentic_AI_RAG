from typing import Tuple, List
from .events import Event, EventType, WorkflowState
from llama_index.core.schema import NodeWithScore

class ValidationStep:
    @staticmethod
    def execute(state: WorkflowState) -> Tuple[WorkflowState, Event]:
        query = state.query.strip()
        
        if not query:
            state.error = "Empty query"
            return state, Event(
                type=EventType.QUERY_INVALID,
                data={"reason": "empty_query"}
            )
        
        if len(query) < 3:
            state.error = "Query too short"
            return state, Event(
                type=EventType.QUERY_INVALID,
                data={"reason": "query_too_short", "length": len(query)}
            )
        
        state.validated = True
        return state, Event(
            type=EventType.QUERY_VALIDATED,
            data={"query": query, "length": len(query)}
        )

class RetrievalStep:
    def __init__(self, retriever, top_k: int = 5):
        self.retriever = retriever
        self.top_k = top_k
        self.confidence_threshold = 0.3
    
    def execute(self, state: WorkflowState) -> Tuple[WorkflowState, Event]:
        try:
            nodes = self.retriever.retrieve(state.query)
            
            if not nodes:
                state.error = "No results found"
                return state, Event(
                    type=EventType.RETRIEVAL_FAILED,
                    data={"reason": "no_results"}
                )
            
            state.retrieved_nodes = nodes
            
            avg_score = sum(node.score for node in nodes) / len(nodes)
            state.confidence_score = avg_score
            
            if avg_score < self.confidence_threshold:
                state.needs_more_context = True
                return state, Event(
                    type=EventType.LOW_CONFIDENCE,
                    data={
                        "score": avg_score,
                        "threshold": self.confidence_threshold,
                        "num_results": len(nodes)
                    }
                )
            
            return state, Event(
                type=EventType.RETRIEVAL_COMPLETED,
                data={
                    "num_results": len(nodes),
                    "avg_score": avg_score
                }
            )
        
        except Exception as e:
            state.error = str(e)
            return state, Event(
                type=EventType.RETRIEVAL_FAILED,
                data={"error": str(e)}
            )

class SynthesisStep:
    def __init__(self, response_synthesizer):
        self.response_synthesizer = response_synthesizer
    
    def execute(self, state: WorkflowState) -> Tuple[WorkflowState, Event]:
        try:
            if not state.retrieved_nodes:
                state.error = "No nodes to synthesize"
                return state, Event(
                    type=EventType.SYNTHESIS_FAILED,
                    data={"reason": "no_nodes"}
                )
            
            response = self.response_synthesizer.synthesize(
                state.query,
                nodes=state.retrieved_nodes
            )
            
            state.response = str(response)
            
            state.sources = []
            for node in state.retrieved_nodes[:3]:
                source_info = {
                    "text": node.node.text[:200] + "...",
                    "score": node.score,
                    "metadata": node.node.metadata
                }
                state.sources.append(source_info)
            
            return state, Event(
                type=EventType.SYNTHESIS_COMPLETED,
                data={
                    "response_length": len(state.response),
                    "num_sources": len(state.sources)
                }
            )
        
        except Exception as e:
            state.error = str(e)
            return state, Event(
                type=EventType.SYNTHESIS_FAILED,
                data={"error": str(e)}
            )

class PostProcessingStep:
    @staticmethod
    def execute(state: WorkflowState) -> Tuple[WorkflowState, Event]:
        if state.needs_more_context:
            context_note = "\n\n⚠️ **הערה:** רמת הביטחון בתשובה נמוכה. ייתכן שיש צורך במידע נוסף."
            state.response += context_note
        
        return state, Event(
            type=EventType.RESPONSE_READY,
            data={
                "final_response": state.response,
                "confidence": state.confidence_score
            }
        )
