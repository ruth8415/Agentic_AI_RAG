# 📦 הוראות התקנה מפורטות

## דרישות מקדימות

- Python 3.9 ואילך
- pip (מנהל חבילות Python)
- חשבון Cohere (חינמי)
- חשבון Pinecone (חינמי)
- MongoDB (אופציונלי - רק לשלב ג')

## שלב 1: הורדת הפרויקט

### אופציה א': Clone מ-Git
```bash
git clone https://github.com/your-username/RAG.git
cd RAG
```

### אופציה ב': הורדה ידנית
1. הורד את הקבצים
2. חלץ לתיקייה
3. פתח terminal בתיקייה

## שלב 2: יצירת סביבה וירטואלית (מומלץ)

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## שלב 3: התקנת תלויות

```bash
pip install -r requirements.txt
```

או התקנה עם setup.py:
```bash
pip install -e .
```

## שלב 4: קבלת API Keys

### Cohere
1. גש ל-https://dashboard.cohere.com/
2. צור חשבון (חינמי)
3. לך ל-API Keys
4. העתק את המפתח

### Pinecone
1. גש ל-https://app.pinecone.io/
2. צור חשבון (חינמי)
3. צור פרויקט חדש
4. העתק את:
   - API Key
   - Environment (למשל: us-east-1)

## שלב 5: הגדרת משתני סביבה

צור קובץ `.env` בתיקיית הפרויקט:

```bash
cp .env.example .env
```

ערוך את `.env`:
```
COHERE_API_KEY=your_actual_cohere_key_here
PINECONE_API_KEY=your_actual_pinecone_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=agentic-coding-docs
```

## שלב 6: הכנת נתונים

### אופציה א': פרויקט קיים
אם יש לך פרויקט עם כלי Agentic Coding, וודא שיש תיקיות:
- `.cursor/` או `.cursorrules/`
- `.windsurf/`
- `.claude/`

### אופציה ב': יצירת נתונים לדוגמה
```bash
mkdir -p test_project/.windsurf/workflows
echo "# Installation Guide" > test_project/.windsurf/README.md
echo "# Project Spec" > test_project/.windsurf/spec.md
echo "# Decisions" > test_project/.windsurf/decisions.md
```

## שלב 7: בדיקת התקנה

```bash
python -c "import llama_index; import cohere; import pinecone; print('All imports successful!')"
```

## שלב 8: הרצה ראשונה

```bash
python run_all_stages.py
```

או הרץ ישירות:
```bash
python main_stage_c.py
```

## MongoDB (אופציונלי - לשלב ג')

### Windows
1. הורד מ-https://www.mongodb.com/try/download/community
2. התקן
3. הרץ MongoDB Compass או:
```bash
mongod
```

### macOS (עם Homebrew)
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

### Linux (Ubuntu)
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

## בדיקת תקינות

לאחר ההתקנה, בדוק:

1. ✅ Python version:
```bash
python --version
```

2. ✅ חבילות מותקנות:
```bash
pip list | grep llama-index
```

3. ✅ משתני סביבה:
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Cohere:', 'OK' if os.getenv('COHERE_API_KEY') else 'Missing')"
```

## פתרון בעיות התקנה

### שגיאה: pip לא מזוהה
```bash
python -m pip install --upgrade pip
```

### שגיאה: Permission denied
```bash
pip install --user -r requirements.txt
```

### שגיאה: SSL Certificate
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## הרצה ראשונה מוצלחת

אם הכל עבד, תראה:
```
=== Stage C: Data Extraction & Hybrid Query System ===

1. Loading documents...
2. Creating vector index...
3. Extracting structured data...
4. Launching Gradio interface...

Running on local URL:  http://127.0.0.1:7860
```

פתח את הדפדפן בכתובת המוצגת ותתחיל לשאול שאלות! 🎉
