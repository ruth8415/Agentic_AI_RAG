# שלב ב' - Event-Driven Workflow

## תיאור

שלב זה משכתב את ה-MVP לארכיטקטורה מבוססת אירועים עם שלבים מוגדרים.

## רכיבים

### events.py
הגדרות אירועים ומצב.

**EventType:**
- QUERY_RECEIVED
- QUERY_VALIDATED
- QUERY_INVALID
- RETRIEVAL_COMPLETED
- RETRIEVAL_FAILED
- LOW_CONFIDENCE
- SYNTHESIS_COMPLETED
- SYNTHESIS_FAILED
- RESPONSE_READY
- ERROR_OCCURRED

**WorkflowState:**
- query, validated, retrieved_nodes
- confidence_score, needs_more_context
- response, sources, error

### workflow_steps.py
שלבי עבודה.

**ValidationStep:**
- בדיקת תקינות שאלה
- בדיקת אורך מינימלי

**RetrievalStep:**
- חיפוש סמנטי
- בדיקת confidence
- זיהוי ביטחון נמוך

**SynthesisStep:**
- יצירת תשובה
- חילוץ מקורות

**PostProcessingStep:**
- הוספת אזהרות
- עיצוב סופי

### workflow_engine.py
מנוע ניהול זרימה.

**תכונות:**
- Event handlers
- State management
- Event logging
- Error handling

## הרצה

```bash
python main_stage_b.py
```
