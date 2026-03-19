import pytest
from pathlib import Path
from src.stage_a_mvp.data_loader import AgenticDocsLoader
from src.stage_b_event_driven.events import Event, EventType, WorkflowState
from src.stage_b_event_driven.workflow_steps import ValidationStep

def test_validation_step_valid_query():
    state = WorkflowState(query="מה הצבע העיקרי?")
    new_state, event = ValidationStep.execute(state)
    
    assert new_state.validated == True
    assert event.type == EventType.QUERY_VALIDATED

def test_validation_step_empty_query():
    state = WorkflowState(query="")
    new_state, event = ValidationStep.execute(state)
    
    assert new_state.validated == False
    assert event.type == EventType.QUERY_INVALID
    assert new_state.error == "Empty query"

def test_validation_step_short_query():
    state = WorkflowState(query="מה")
    new_state, event = ValidationStep.execute(state)
    
    assert new_state.validated == False
    assert event.type == EventType.QUERY_INVALID

def test_workflow_state_initialization():
    state = WorkflowState()
    
    assert state.query == ""
    assert state.validated == False
    assert state.retrieved_nodes == []
    assert state.sources == []
    assert state.confidence_score == 0.0

def test_event_creation():
    event = Event(
        type=EventType.QUERY_RECEIVED,
        data={"query": "test"}
    )
    
    assert event.type == EventType.QUERY_RECEIVED
    assert event.data["query"] == "test"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
