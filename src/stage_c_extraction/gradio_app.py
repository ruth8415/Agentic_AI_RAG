import gradio as gr
from typing import List, Tuple
from .router import HybridQueryRouter

class GradioHybridInterface:
    def __init__(self, router: HybridQueryRouter):
        self.router = router
    
    def chat(self, message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
        if not message.strip():
            return "", history
        
        result = self.router.route_query(message)
        
        answer = result["answer"]
        query_type = result.get("query_type", "unknown")
        
        if result.get("sources"):
            sources_text = f"\n\n**מקורות ({query_type}):**\n"
            
            for i, source in enumerate(result["sources"][:3], 1):
                if query_type == "semantic":
                    tool = source["metadata"].get("tool", "Unknown")
                    file = source["metadata"].get("relative_path", "Unknown")
                    score = source.get("score", 0)
                    sources_text += f"{i}. {tool} - {file} (Score: {score:.2f})\n"
                else:
                    source_info = source.get("source", {})
                    tool = source_info.get("tool", "Unknown")
                    file = source_info.get("file", "Unknown")
                    sources_text += f"{i}. {tool} - {file}\n"
            
            full_answer = answer + sources_text
        else:
            full_answer = answer
        
        if "confidence" in result and result["confidence"] > 0:
            full_answer += f"\n\n**רמת ביטחון:** {result['confidence']:.2%}"
        
        if "item_count" in result:
            full_answer += f"\n**פריטים שנמצאו:** {result['item_count']}"
        
        full_answer += f"\n\n_סוג שאילתה: {query_type}_"
        
        history.append((message, full_answer))
        
        return "", history
    
    def create_interface(self) -> gr.Blocks:
        with gr.Blocks(title="RAG - Hybrid Query System", theme=gr.themes.Soft()) as demo:
            gr.Markdown("""
            # 🤖 RAG - Agentic Coding Documentation Assistant (Hybrid)
            
            **שלב ג' - מערכת היברידית עם Data Extraction**
            
            המערכת תומכת בשני סוגי חיפוש:
            - 🔍 **חיפוש סמנטי** - לשאלות כלליות על התיעוד
            - 📊 **חיפוש מובנה** - לשאלות רשימתיות, עדכניות או מבוססות זמן
            
            **דוגמאות לשאלות סמנטיות:**
            - איך מתקינים את המערכת?
            - מה הצבע העיקרי שנבחר?
            
            **דוגמאות לשאלות מובנות:**
            - תן לי רשימה של כל ההחלטות הטכניות
            - מה ההנחיה העדכנית לגבי RTL?
            - אילו אזהרות נוספו בשבוע האחרון?
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
