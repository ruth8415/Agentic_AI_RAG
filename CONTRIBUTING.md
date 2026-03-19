# 🤝 תרומה לפרויקט

## איך לתרום?

### דיווח על באגים

1. בדוק אם הבאג כבר דווח ב-Issues
2. פתח Issue חדש עם:
   - תיאור הבעיה
   - שלבים לשחזור
   - התנהגות צפויה vs. התנהגות בפועל
   - סביבת העבודה (OS, Python version)

### הצעת פיצ'רים

1. פתח Issue עם תיאור הפיצ'ר
2. הסבר למה זה שימושי
3. הצע מימוש אפשרי

### תרומת קוד

#### 1. Fork & Clone
```bash
git clone https://github.com/your-username/RAG.git
cd RAG
```

#### 2. יצירת Branch
```bash
git checkout -b feature/your-feature-name
```

#### 3. פיתוח
- עקוב אחר סגנון הקוד הקיים
- הוסף docstrings לפונקציות חדשות
- כתוב בדיקות לקוד חדש

#### 4. בדיקות
```bash
pytest tests/
```

#### 5. Commit
```bash
git add .
git commit -m "Add: your feature description"
```

#### 6. Push & Pull Request
```bash
git push origin feature/your-feature-name
```

פתח Pull Request עם תיאור מפורט

## סגנון קוד

- Python 3.9+
- PEP 8
- Type hints כשאפשר
- Docstrings בעברית או אנגלית

## מבנה Commit Messages

```
Add: הוספת פיצ'ר חדש
Fix: תיקון באג
Update: עדכון קוד קיים
Docs: שינוי בתיעוד
Test: הוספת בדיקות
```

## תחומים לתרומה

- [ ] תמיכה בכלי Agentic Coding נוספים
- [ ] שיפור דיוק הסיווג
- [ ] אופטימיזציה של ביצועים
- [ ] תיעוד נוסף
- [ ] בדיקות נוספות
- [ ] UI/UX שיפורים

## שאלות?

פתח Discussion או שלח Issue
