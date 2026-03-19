import sys
from pathlib import Path

def print_menu():
    print("\n" + "="*60)
    print("🤖 RAG - Agentic Coding Documentation Assistant")
    print("="*60)
    print("\nבחר שלב להרצה:\n")
    print("1. שלב א' - MVP: חיפוש סמנטי בסיסי")
    print("2. שלב ב' - Event-Driven Workflow")
    print("3. שלב ג' - Hybrid Query System (מומלץ)")
    print("4. יציאה")
    print("\n" + "="*60)

def main():
    while True:
        print_menu()
        choice = input("\nהזן מספר (1-4): ").strip()
        
        if choice == "1":
            print("\n🚀 מריץ שלב א' - MVP...")
            import main_stage_a
            main_stage_a.main()
            break
        
        elif choice == "2":
            print("\n🚀 מריץ שלב ב' - Event-Driven...")
            import main_stage_b
            main_stage_b.main()
            break
        
        elif choice == "3":
            print("\n🚀 מריץ שלב ג' - Hybrid System...")
            import main_stage_c
            main_stage_c.main()
            break
        
        elif choice == "4":
            print("\n👋 להתראות!")
            sys.exit(0)
        
        else:
            print("\n❌ בחירה לא תקינה. נסה שוב.")

if __name__ == "__main__":
    main()
