from typing import Callable, Dict, List
from .events import Event, EventType, WorkflowState
from .workflow_steps import ValidationStep, RetrievalStep, SynthesisStep, PostProcessingStep

class WorkflowEngine:
    def __init__(self, retriever, response_synthesizer):
        self.validation_step = ValidationStep()
        self.retrieval_step = RetrievalStep(retriever)
        self.synthesis_step = SynthesisStep(response_synthesizer)
        self.post_processing_step = PostProcessingStep()
        
        self.event_handlers = self._setup_event_handlers()
        self.event_log = []
    
    def _setup_event_handlers(self) -> Dict[EventType, Callable]:
        return {
            EventType.QUERY_RECEIVED: self._handle_query_received,
            EventType.QUERY_VALIDATED: self._handle_query_validated,
            EventType.QUERY_INVALID: self._handle_query_invalid,
            EventType.RETRIEVAL_COMPLETED: self._handle_retrieval_completed,
            EventType.RETRIEVAL_FAILED: self._handle_retrieval_failed,
            EventType.LOW_CONFIDENCE: self._handle_low_confidence,
            EventType.SYNTHESIS_COMPLETED: self._handle_synthesis_completed,
            EventType.SYNTHESIS_FAILED: self._handle_synthesis_failed,
        }
    
    def process_query(self, query: str) -> Dict:
        state = WorkflowState(query=query)
        
        initial_event = Event(
            type=EventType.QUERY_RECEIVED,
            data={"query": query}
        )
        
        self.event_log = [initial_event]
        
        state, final_event = self._process_event(state, initial_event)
        
        return {
            "answer": state.response,
            "sources": state.sources,
            "confidence": state.confidence_score,
            "error": state.error,
            "event_log": [str(e) for e in self.event_log]
        }
    
    def _process_event(self, state: WorkflowState, event: Event) -> tuple:
        handler = self.event_handlers.get(event.type)
        
        if not handler:
            return state, Event(
                type=EventType.ERROR_OCCURRED,
                data={"error": f"No handler for {event.type}"}
            )
        
        return handler(state, event)
    
    def _handle_query_received(self, state: WorkflowState, event: Event) -> tuple:
        state, next_event = self.validation_step.execute(state)
        self.event_log.append(next_event)
        
        if next_event.type == EventType.QUERY_INVALID:
            return state, next_event
        
        return self._process_event(state, next_event)
    
    def _handle_query_validated(self, state: WorkflowState, event: Event) -> tuple:
        state, next_event = self.retrieval_step.execute(state)
        self.event_log.append(next_event)
        
        return self._process_event(state, next_event)
    
    def _handle_query_invalid(self, state: WorkflowState, event: Event) -> tuple:
        state.response = f"שאלה לא תקינה: {event.data.get('reason', 'unknown')}"
        return state, Event(type=EventType.ERROR_OCCURRED, data=event.data)
    
    def _handle_retrieval_completed(self, state: WorkflowState, event: Event) -> tuple:
        state, next_event = self.synthesis_step.execute(state)
        self.event_log.append(next_event)
        
        return self._process_event(state, next_event)
    
    def _handle_retrieval_failed(self, state: WorkflowState, event: Event) -> tuple:
        state.response = f"החיפוש נכשל: {event.data.get('reason', 'unknown')}"
        return state, Event(type=EventType.ERROR_OCCURRED, data=event.data)
    
    def _handle_low_confidence(self, state: WorkflowState, event: Event) -> tuple:
        state, next_event = self.synthesis_step.execute(state)
        self.event_log.append(next_event)
        
        return self._process_event(state, next_event)
    
    def _handle_synthesis_completed(self, state: WorkflowState, event: Event) -> tuple:
        state, next_event = self.post_processing_step.execute(state)
        self.event_log.append(next_event)
        
        return state, next_event
    
    def _handle_synthesis_failed(self, state: WorkflowState, event: Event) -> tuple:
        state.response = f"יצירת התשובה נכשלה: {event.data.get('error', 'unknown')}"
        return state, Event(type=EventType.ERROR_OCCURRED, data=event.data)
