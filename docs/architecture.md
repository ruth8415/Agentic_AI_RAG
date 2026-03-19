# 🏗️ ארכיטקטורת המערכת

## סקירה כללית

המערכת בנויה בשלושה שלבים, כאשר כל שלב מוסיף שכבת מורכבות ויכולות:

## שלב א' - MVP

### מטרה
חיפוש סמנטי בסיסי על תיעוד Agentic Coding

### רכיבים

```
┌─────────────────┐
│ AgenticDocsLoader│ → טעינת קבצי MD
└─────────────────┘
         ↓
┌─────────────────┐
│ DocumentIndexer │ → Chunking + Embedding + Pinecone
└─────────────────┘
         ↓
┌─────────────────┐
│ RAGQueryEngine  │ → Retrieval + Synthesis
└─────────────────┘
         ↓
┌─────────────────┐
│  GradioApp      │ → UI
└─────────────────┘
```

### טכנולוגיות
- **LlamaIndex**: Framework ראשי
- **Cohere**: Embeddings + LLM
- **Pinecone**: Vector Store
- **Gradio**: UI

## שלב ב' - Event-Driven

### מטרה
ארכיטקטורה מסודרת עם שלבים ברורים ובדיקות

### רכיבים

```
┌──────────────────────────────────────────┐
│           WorkflowEngine                 │
│  ┌────────────────────────────────────┐  │
│  │  Event Handlers                    │  │
│  │  - QUERY_RECEIVED                  │  │
│  │  - QUERY_VALIDATED                 │  │
│  │  - RETRIEVAL_COMPLETED             │  │
│  │  - SYNTHESIS_COMPLETED             │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
         ↓           ↓           ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Validation   │ │  Retrieval   │ │  Synthesis   │
│    Step      │ │     Step     │ │     Step     │
└──────────────┘ └──────────────┘ └──────────────┘
```

### תכונות מרכזיות
- **State Management**: ניהול מצב לאורך כל התהליך
- **Event-Driven**: כל שלב מפיק אירוע
- **Validation**: בדיקות בכל שלב
- **Confidence Scoring**: זיהוי תשובות בביטחון נמוך

## שלב ג' - Hybrid System

### מטרה
שילוב חיפוש סמנטי עם שליפת נתונים מובנים

### ארכיטקטורה

```
                    User Query
                        ↓
              ┌─────────────────┐
              │ QueryClassifier │
              └─────────────────┘
                        ↓
              ┌─────────────────┐
              │ HybridRouter    │
              └─────────────────┘
                   ↙        ↘
        ┌──────────┐      ┌──────────────┐
        │ Semantic │      │  Structured  │
        │  Search  │      │    Query     │
        └──────────┘      └──────────────┘
             ↓                    ↓
        ┌──────────┐      ┌──────────────┐
        │ Pinecone │      │ JSON/MongoDB │
        └──────────┘      └──────────────┘
                   ↘        ↙
              ┌─────────────────┐
              │  LLM Synthesis  │
              └─────────────────┘
                        ↓
                   Final Answer
```

### רכיבים חדשים

#### 1. Schema (Pydantic Models)
```python
- Decision
- Rule
- Warning
- Dependency
- Change
```

#### 2. StructuredDataExtractor
חילוץ נתונים מובנים מהמסמכים באמצעות LLM

#### 3. QueryClassifier
סיווג שאילתות לפי סוג:
- `SEMANTIC` - חיפוש סמנטי
- `STRUCTURED_LIST` - רשימה מלאה
- `STRUCTURED_LATEST` - מידע עדכני
- `STRUCTURED_TIME_BASED` - מבוסס זמן

#### 4. HybridRouter
ניתוב חכם בין שני סוגי החיפוש

## זרימת נתונים

### Indexing Flow
```
MD Files → Load → Chunk → Embed → Pinecone
                     ↓
                  Extract → Schema → JSON/MongoDB
```

### Query Flow
```
User Query → Classify → Route
                          ↓
              ┌───────────┴───────────┐
              ↓                       ↓
         Semantic                Structured
              ↓                       ↓
         Pinecone                JSON/DB
              ↓                       ↓
              └───────────┬───────────┘
                          ↓
                    Synthesize
                          ↓
                       Answer
```

## החלטות עיצוב

### למה Event-Driven?
- **Modularity**: כל שלב עצמאי
- **Testability**: קל לבדוק כל שלב
- **Extensibility**: קל להוסיף שלבים
- **Debugging**: קל לעקוב אחר הזרימה

### למה Hybrid?
- חיפוש סמנטי מצוין לשאלות כלליות
- שליפה מובנית מדויקת יותר לשאלות ספציפיות
- שילוב מאפשר לענות על טווח רחב של שאלות

### למה Pydantic?
- Type safety
- Validation אוטומטית
- JSON serialization מובנה
- תיעוד עצמי

## ביצועים

### Latency
- **Semantic Search**: ~2-3 שניות
- **Structured Query**: ~1-2 שניות
- **Hybrid**: תלוי בסוג השאילתה

### Scalability
- **Documents**: עד 10,000 מסמכים
- **Queries**: ללא הגבלה (stateless)
- **Concurrent Users**: תלוי ב-Gradio server

## אבטחה

- API Keys ב-`.env` (לא ב-Git)
- Validation של קלט משתמש
- Rate limiting (ניתן להוסיף)
- Error handling מקיף
