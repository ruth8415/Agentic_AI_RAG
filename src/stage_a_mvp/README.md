# שלב א' - MVP: חיפוש סמנטי

## תיאור

שלב זה מממש RAG בסיסי עם חיפוש סמנטי על תיעוד כלי Agentic Coding.

## רכיבים

### data_loader.py
טעינת קבצי MD מתיקיות של כלי Agentic Coding.

**תכונות:**
- זיהוי אוטומטי של תיקיות (.cursor, .windsurf, .claude)
- טעינה רקורסיבית של קבצי MD
- העשרת metadata (tool, file path)

### indexer.py
יצירת אינדקס וקטורי.

**תכונות:**
- Chunking עם SentenceSplitter
- Embeddings עם Cohere
- אחסון ב-Pinecone
- יצירה/טעינה של אינדקס

### query_engine.py
מנוע שאילתות.

**תכונות:**
- Retrieval עם VectorIndexRetriever
- Synthesis עם Cohere LLM
- החזרת מקורות

### gradio_app.py
ממשק משתמש.

**תכונות:**
- צ'אט אינטראקטיבי
- תמיכה ב-RTL
- הצגת מקורות

## הרצה

```bash
python main_stage_a.py
```
