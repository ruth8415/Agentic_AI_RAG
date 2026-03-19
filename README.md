# 🤖 RAG - Agentic Coding Documentation Assistant

## 📌 תיאור הפרויקט

מערכת RAG מתקדמת לניתוח ותשאול תיעוד של כלי Agentic Coding (Cursor, Windsurf, Claude Code).

המערכת סורקת את קבצי ה-Markdown שכלי הקידוד יוצרים, מאנדקסת אותם, ומאפשרת לשאול שאלות ולקבל תשובות מבוססות על המידע שנצבר.

## 🎯 מטרות הפרויקט

1. **הבנת הקשר** - לאפשר למתכנתים להבין על מה מתבססים כלי ה-AI בקבלת החלטות
2. **Onboarding מהיר** - לעזור למתכנתים חדשים להבין את הפרויקט במהירות
3. **מעקב אחר שינויים** - לעקוב אחר החלטות, כללים ושינויים בפרויקט

## 🛠️ טכנולוגיות

- **LlamaIndex** - Framework לבניית יישומי RAG
- **Cohere** - מודלי Embedding ו-LLM
- **Pinecone** - מסד נתונים וקטורי
- **Gradio** - ממשק משתמש
- **MongoDB** (אופציונלי) - אחסון נתונים מובנים
- **Pydantic** - ולידציה וסכמות

## 📊 שלבי הפרויקט

### שלב א' - MVP: חיפוש סמנטי

**קבצים:**
- `main_stage_a.py` - נקודת כניסה
- `src/stage_a_mvp/` - כל הקוד

**תכונות:**
- טעינת קבצי MD מכלי Agentic Coding
- חיתוך למקטעים (Chunking)
- יצירת Embeddings עם Cohere
- אחסון ב-Pinecone
- חיפוש סמנטי ויצירת תשובות
- ממשק Gradio

**הרצה:**
```bash
python main_stage_a.py
```

### שלב ב' - Event-Driven Workflow

**קבצים:**
- `main_stage_b.py` - נקודת כניסה
- `src/stage_b_event_driven/` - כל הקוד

**תכונות:**
- ארכיטקטורה מבוססת אירועים
- שלבי עבודה מוגדרים: Validation → Retrieval → Synthesis → Post-Processing
- ניהול State ו-Events
- בדיקות תקינות ולידציות
- זיהוי רמת ביטחון נמוכה

**הרצה:**
```bash
python main_stage_b.py
```

### שלב ג' - Data Extraction & Hybrid Query

**קבצים:**
- `main_stage_c.py` - נקודת כניסה
- `src/stage_c_extraction/` - כל הקוד

**תכונות:**
- חילוץ נתונים מובנים (Decisions, Rules, Warnings, Dependencies, Changes)
- סכמה מוגדרת עם Pydantic
- אחסון ב-JSON או MongoDB
- סיווג שאילתות אוטומטי
- ניתוב חכם בין חיפוש סמנטי למובנה
- תמיכה בשאילתות רשימתיות, עדכניות ומבוססות זמן

**הרצה:**
```bash
python main_stage_c.py
```

## 🚀 התקנה והרצה

### 1. התקנת תלויות

```bash
pip install -r requirements.txt
```

### 2. הגדרת משתני סביבה

העתק את `.env.example` ל-`.env` ומלא את הערכים:

```bash
COHERE_API_KEY=your_cohere_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=agentic-coding-docs
```

### 3. הכנת נתונים

וודא שיש לך פרויקט עם תיקיות של כלי Agentic Coding:
- `.cursor/` או `.cursorrules/`
- `.windsurf/`
- `.claude/`

### 4. הרצת המערכת

בחר את השלב הרצוי:

```bash
# שלב א' - MVP
python main_stage_a.py

# שלב ב' - Event-Driven
python main_stage_b.py

# שלב ג' - Hybrid (מומלץ)
python main_stage_c.py
```

הממשק יפתח בכתובת: http://127.0.0.1:7860

## 💡 דוגמאות לשאלות

### שאלות סמנטיות (כל השלבים)
- "איך מתקינים את המערכת?"
- "מה הצבע העיקרי שנבחר לדיזיין?"
- "מה הארכיטקטורה של המערכת?"

### שאלות מובנות (שלב ג' בלבד)
- "תן לי רשימה של כל ההחלטות הטכניות"
- "מה ההנחיה העדכנית לגבי RTL בממשק?"
- "אילו אזהרות נוספו בשבוע האחרון?"
- "הצג את כל הכללים הקשורים ל-UI"

## 📁 מבנה הפרויקט

```
RAG/
├── config.py                      # הגדרות כלליות
├── requirements.txt               # תלויות
├── .env.example                   # דוגמה למשתני סביבה
├── main_stage_a.py               # שלב א'
├── main_stage_b.py               # שלב ב'
├── main_stage_c.py               # שלב ג'
├── src/
│   ├── stage_a_mvp/              # שלב א' - MVP
│   │   ├── data_loader.py        # טעינת מסמכים
│   │   ├── indexer.py            # יצירת אינדקס
│   │   ├── query_engine.py       # מנוע שאילתות
│   │   └── gradio_app.py         # ממשק משתמש
│   ├── stage_b_event_driven/     # שלב ב' - Event-Driven
│   │   ├── events.py             # הגדרות אירועים
│   │   ├── workflow_steps.py     # שלבי עבודה
│   │   ├── workflow_engine.py    # מנוע Workflow
│   │   └── gradio_app.py         # ממשק משתמש
│   └── stage_c_extraction/       # שלב ג' - Data Extraction
│       ├── schema.py             # סכמות נתונים
│       ├── extractor.py          # חילוץ נתונים
│       ├── storage.py            # אחסון
│       ├── query_classifier.py   # סיווג שאילתות
│       ├── router.py             # ניתוב
│       └── gradio_app.py         # ממשק משתמש
├── docs/
│   ├── workflow_diagram.html     # תרשים זרימה
│   └── reflection.md             # רפלקציה
└── README.md                      # מסמך זה
```

## 🔍 ארכיטקטורה

### שלב א' - MVP
```
Documents → Chunking → Embeddings → Pinecone → Retrieval → Synthesis → Answer
```

### שלב ב' - Event-Driven
```
Query → Validation → Retrieval → Confidence Check → Synthesis → Post-Processing → Response
         ↓              ↓                ↓              ↓              ↓
       Events        Events           Events         Events         Events
```

### שלב ג' - Hybrid
```
Query → Classification → Router
                          ├─→ Semantic Search (Pinecone) → Answer
                          └─→ Structured Query (JSON/MongoDB) → Answer
```

## 🧪 בדיקות ולידציות

המערכת כוללת בדיקות בכל שלב:

1. **Validation** - בדיקת תקינות השאלה
2. **Confidence Check** - בדיקת רמת ביטחון בתוצאות
3. **Error Handling** - טיפול בשגיאות בכל שלב
4. **Query Classification** - סיווג אוטומטי של סוג השאילתה

## 📈 שיפורים עתידיים

- [ ] סנכרון אוטומטי של שינויים בקבצים
- [ ] תמיכה בכלי Agentic Coding נוספים
- [ ] ממשק ניהול למעקב אחר חילוצי נתונים
- [ ] אינטגרציה עם Git לזיהוי שינויים
- [ ] תמיכה בשפות נוספות
- [ ] מערכת Caching לשיפור ביצועים

## 🤝 תרומה

הפרויקט פתוח לתרומות! אפשר:
- לדווח על באגים
- להציע פיצ'רים חדשים
- לשפר את התיעוד
- להוסיף תמיכה בכלים נוספים

## 📝 רישיון

MIT License - ראה קובץ LICENSE לפרטים

## 👥 יוצרים

פרויקט נוצר כחלק מקורס RAG עם LlamaIndex

---

**אם אחרי הפרויקט את מוצאת את עצמך שואלת: "איפה עוד אפשר ליישם את זה" — זה ראג ההתחלה 🛣️**
