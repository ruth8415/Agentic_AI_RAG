# 🔧 פתרון בעיות

## בעיות נפוצות ופתרונות

### 1. שגיאות API Key

#### בעיה
```
Error: COHERE_API_KEY not found
```

#### פתרון
1. צור קובץ `.env` בתיקיית הפרויקט
2. הוסף:
```
COHERE_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
```
3. וודא שהקובץ נמצא באותה תיקייה כמו `main_stage_*.py`

---

### 2. Pinecone Index לא נמצא

#### בעיה
```
Error: Index 'agentic-coding-docs' not found
```

#### פתרון
המערכת תיצור את ה-Index אוטומטית בהרצה הראשונה.
אם זה לא עובד:
1. בדוק ש-PINECONE_API_KEY תקין
2. בדוק את PINECONE_ENVIRONMENT (צריך להיות region תקין כמו `us-east-1`)

---

### 3. לא נמצאו מסמכים

#### בעיה
```
Warning: No documents found
No agentic tool directories found in /path/to/project
```

#### פתרון
1. וודא שהנתיב שהזנת מכיל תיקיות של כלי Agentic Coding:
   - `.cursor/` או `.cursorrules/`
   - `.windsurf/`
   - `.claude/`

2. בדוק שיש קבצי `.md` בתיקיות אלו

3. אם אין לך פרויקט כזה, צור תיקייה לדוגמה:
```bash
mkdir -p test_project/.windsurf
echo "# Test Doc" > test_project/.windsurf/test.md
```

---

### 4. שגיאות Gradio

#### בעיה
```
Error: Port 7860 already in use
```

#### פתרון
1. סגור תהליכים אחרים על פורט 7860
2. או שנה את הפורט בקוד:
```python
app.launch(server_port=7861)
```

---

### 5. שגיאות Embedding

#### בעיה
```
Error: Embedding failed
```

#### פתרון
1. בדוק חיבור לאינטרנט
2. בדוק שה-API Key של Cohere תקין
3. בדוק שיש לך מספיק credits ב-Cohere

---

### 6. MongoDB Connection Error

#### בעיה (שלב ג' בלבד)
```
Error: Could not connect to MongoDB
```

#### פתרון
1. אם אתה משתמש ב-MongoDB מקומי, וודא שהוא רץ:
```bash
mongod
```

2. או השתמש ב-JSON storage במקום:
```python
router = HybridQueryRouter(semantic_engine, storage_type="json")
```

---

### 7. תשובות לא רלוונטיות

#### בעיה
המערכת מחזירה תשובות לא רלוונטיות

#### פתרון
1. בדוק את `CHUNK_SIZE` ב-`config.py` - נסה להקטין ל-256 או להגדיל ל-1024
2. שנה את `top_k` - נסה 3 או 10 במקום 5
3. וודא שהמסמכים מכילים מידע רלוונטי

---

### 8. ביצועים איטיים

#### בעיה
המערכת איטית מדי

#### פתרון
1. הקטן את מספר המסמכים בהרצה ראשונה
2. השתמש ב-caching (ניתן להוסיף)
3. בדוק חיבור לאינטרנט
4. שקול להשתמש במודל Cohere קטן יותר

---

### 9. שגיאות בחילוץ נתונים (שלב ג')

#### בעיה
```
Error extracting decisions/rules/warnings
```

#### פתרון
1. זה תקין - לא כל מסמך מכיל את כל סוגי הפריטים
2. בדוק את הלוגים לראות כמה פריטים חולצו בהצלחה
3. אם אף פריט לא חולץ, בדוק שהמסמכים מכילים מידע רלוונטי

---

### 10. Import Errors

#### בעיה
```
ModuleNotFoundError: No module named 'llama_index'
```

#### פתרון
```bash
pip install -r requirements.txt
```

או התקן ידנית:
```bash
pip install llama-index llama-index-llms-cohere llama-index-embeddings-cohere
```

---

## עדיין יש בעיה?

1. בדוק את הלוגים המלאים
2. חפש בעיות דומות ב-Issues
3. פתח Issue חדש עם:
   - תיאור הבעיה
   - הלוגים המלאים
   - סביבת העבודה (OS, Python version)
   - שלבי השחזור
