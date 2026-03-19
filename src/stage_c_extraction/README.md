# שלב ג' - Data Extraction & Hybrid Query

## תיאור

שלב זה מוסיף חילוץ נתונים מובנים וניתוב חכם בין חיפוש סמנטי למובנה.

## רכיבים

### schema.py
סכמות Pydantic.

**מודלים:**
- Decision - החלטות טכניות
- Rule - כללים והנחיות
- Warning - אזהרות ורגישויות
- Dependency - תלויות
- Change - שינויים חשובים

### extractor.py
חילוץ נתונים מובנים.

**תכונות:**
- LLM-based extraction
- תמיכה בכל סוגי הפריטים
- Metadata enrichment

### storage.py
אחסון נתונים.

**JSONStorage:**
- שמירה/טעינה מ-JSON
- פשוט ומהיר

**MongoDBStorage:**
- שמירה/טעינה מ-MongoDB
- שאילתות מתקדמות

### query_classifier.py
סיווג שאילתות.

**QueryType:**
- SEMANTIC - חיפוש סמנטי
- STRUCTURED_LIST - רשימה מלאה
- STRUCTURED_LATEST - מידע עדכני
- STRUCTURED_TIME_BASED - מבוסס זמן

### router.py
ניתוב היברידי.

**תכונות:**
- סיווג אוטומטי
- ניתוב לחיפוש מתאים
- Synthesis מאוחד

## הרצה

```bash
python main_stage_c.py
```
