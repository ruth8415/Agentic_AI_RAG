# 🚀 התחלה מהירה

## התקנה בשלושה שלבים

### 1. התקנת תלויות
```bash
pip install -r requirements.txt
```

### 2. הגדרת API Keys

צור קובץ `.env` בתיקיית הפרויקט:

```bash
COHERE_API_KEY=your_cohere_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=us-east-1
```

**איך להשיג API Keys:**

- **Cohere**: https://dashboard.cohere.com/api-keys
- **Pinecone**: https://app.pinecone.io/

### 3. הרצה

```bash
python run_all_stages.py
```

או הרץ ישירות שלב ג' (המתקדם ביותר):

```bash
python main_stage_c.py
```

## דוגמאות לשאלות

### שאלות סמנטיות
```
איך מתקינים את המערכת?
מה הצבע העיקרי שנבחר?
הסבר את הארכיטקטורה
```

### שאלות מובנות (שלב ג')
```
תן לי רשימה של כל ההחלטות
מה ההנחיה העדכנית לגבי RTL?
אילו אזהרות נוספו בשבוע האחרון?
```

## פתרון בעיות נפוצות

### שגיאת API Key
```
Error: COHERE_API_KEY not found
```
**פתרון:** וודא שיצרת קובץ `.env` עם המפתחות

### Pinecone Index לא קיים
```
Error: Index not found
```
**פתרון:** המערכת תיצור אוטומטית את ה-Index בהרצה הראשונה

### לא נמצאו מסמכים
```
Warning: No documents found
```
**פתרון:** וודא שהנתיב לפרויקט מכיל תיקיות `.cursor/`, `.windsurf/` או `.claude/`

## עזרה נוספת

ראה `README.md` לתיעוד מלא
