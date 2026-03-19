import gradio as gr
from typing import List, Tuple
from .query_engine import RAGQueryEngine
from .indexer import DocumentIndexer

class GradioRAGInterface:
    def __init__(self, query_engine: RAGQueryEngine):
        self.query_engine = query_engine
        self.chat_history = []
    
    def chat(self, message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
        if not message.strip():
            return "", history
        
        result = self.query_engine.query(message)
        answer = result["answer"]
        sources = result["sources"]
        
        sources_text = "\n\n**מקורות:**\n"
        for i, source in enumerate(sources[:3], 1):
            tool = source["metadata"].get("tool", "Unknown")
            file = source["metadata"].get("relative_path", "Unknown")
            score = source["score"]
            sources_text += f"{i}. {tool} - {file} (Score: {score:.2f})\n"
        
        full_answer = answer + sources_text
        
        history.append((message, full_answer))
        
        return "", history
    
    def create_interface(self) -> gr.Blocks:
        with gr.Blocks(title="RAG - Agentic Coding Docs", theme=gr.themes.Soft()) as demo:
            gr.Markdown("""
            # 🤖 RAG - Agentic Coding Documentation Assistant
            
            שאל שאלות על תיעוד כלי ה-Agentic Coding שלך (Cursor, Windsurf, Claude Code)
            
            **דוגמאות לשאלות:**
            - מה הצבע העיקרי שנבחר לדיזיין של המערכת?
            - איך מתקינים את המערכת?
            - מה ההחלטות הטכניות החשובות שהתקבלו?
            - האם יש הנחיות לגבי RTL?
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
