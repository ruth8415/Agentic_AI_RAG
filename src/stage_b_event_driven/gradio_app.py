import gradio as gr
from typing import List, Tuple
from .workflow_engine import WorkflowEngine

class GradioEventDrivenInterface:
    def __init__(self, workflow_engine: WorkflowEngine):
        self.workflow_engine = workflow_engine
    
    def chat(self, message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
        if not message.strip():
            return "", history
        
        result = self.workflow_engine.process_query(message)
        
        answer = result["answer"]
        sources = result["sources"]
        confidence = result["confidence"]
        
        if sources:
            sources_text = "\n\n**מקורות:**\n"
            for i, source in enumerate(sources[:3], 1):
                tool = source["metadata"].get("tool", "Unknown")
                file = source["metadata"].get("relative_path", "Unknown")
                score = source["score"]
                sources_text += f"{i}. {tool} - {file} (Score: {score:.2f})\n"
            
            full_answer = answer + sources_text
        else:
            full_answer = answer
        
        if confidence > 0:
            full_answer += f"\n\n**רמת ביטחון:** {confidence:.2%}"
        
        history.append((message, full_answer))
        
        return "", history
    
    def create_interface(self) -> gr.Blocks:
        with gr.Blocks(title="RAG - Event-Driven Workflow", theme=gr.themes.Soft()) as demo:
            gr.Markdown("""
            # 🤖 RAG - Agentic Coding Documentation Assistant (Event-Driven)
            
            **שלב ב' - ארכיטקטורת Event-Driven Workflow**
            
            המערכת עובדת בצורה מסודרת עם שלבים ברורים:
            1. ✅ Validation - בדיקת תקינות השאלה
            2. 🔍 Retrieval - חיפוש סמנטי במסמכים
            3. 🧠 Synthesis - יצירת תשובה
            4. 📊 Post-Processing - עיבוד סופי
            
            **דוגמאות לשאלות:**
            - מה הצבע העיקרי שנבחר לדיזיין של המערכת?
            - איך מתקינים את המערכת?
            - מה ההחלטות הטכניות החשובות שהתקבלו?
            """)
            
            chatbot = gr.Chatbot(
                label="שיחה",
                height=500,
                rtl=True
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    label="שאלה",
                    placeholder="הקלד את שאלתך כאן...",
                    scale=4,
                    rtl=True
                )
                submit = gr.Button("שלח", scale=1)
            
            clear = gr.Button("נקה היסטוריה")
            
            submit.click(
                self.chat,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )
            
            msg.submit(
                self.chat,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot]
            )
            
            clear.click(lambda: [], outputs=[chatbot])
        
        return demo
    
    def launch(self, **kwargs):
        demo = self.create_interface()
        demo.launch(**kwargs)
