"""
גרסה פשוטה של המערכת שעובדת בלי Pinecone - רק עם חיפוש מקומי
"""
from pathlib import Path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere
from llama_index.core.llms import ChatMessage
import gradio as gr
import config

def load_documents():
    """טעינת מסמכים מהפרויקט לדוגמה"""
    project_path = Path(r"C:\Users\user1\Desktop\test_project\.windsurf")
    
    print(f"Loading documents from: {project_path}")
    
    # מצא את כל קבצי ה-MD ידנית
    md_files = list(project_path.glob("*.md"))
    print(f"Found {len(md_files)} .md files")
    
    if not md_files:
        print("No .md files found!")
        return []
    
    reader = SimpleDirectoryReader(
        input_files=[str(f) for f in md_files]
    )
    
    documents = reader.load_data()
    print(f"Loaded {len(documents)} documents")
    
    for doc in documents:
        file_name = Path(doc.metadata.get("file_path", "")).name
        print(f"  - {file_name}")
    
    return documents

def create_index(documents):
    """יצירת אינדקס מקומי (בלי Pinecone)"""
    print("\nCreating embeddings with Cohere...")
    
    from llama_index.core.node_parser import SentenceSplitter
    
    Settings.embed_model = CohereEmbedding(
        api_key=config.COHERE_API_KEY,
        model_name="embed-multilingual-v3.0"
    )
    
    # חלוקה לחלקים קטנים יותר לדיוק טוב יותר
    splitter = SentenceSplitter(chunk_size=256, chunk_overlap=50)
    
    # לא צריך LLM - רק embeddings לחיפוש סמנטי
    
    index = VectorStoreIndex.from_documents(
        documents,
        transformations=[splitter],
        show_progress=True
    )
    
    print("Index created successfully!")
    return index

def create_chat_interface(index):
    """יצירת ממשק Gradio"""
    retriever = index.as_retriever(similarity_top_k=5)
    
    # יצירת LLM לסינתזה של תשובות
    llm = Cohere(
        api_key=config.COHERE_API_KEY,
        model="command-r-08-2024",
        temperature=0.1
    )
    
    def chat(message, history):
        if not message.strip():
            return "", history
        
        print(f"\nQuery: {message}")
        
        # חיפוש סמנטי
        nodes = retriever.retrieve(message)
        
        # סינון תוצאות רלוונטיות
        relevant_nodes = [n for n in nodes if n.score > 0.35]
        
        if not relevant_nodes:
            answer = "לא נמצאו תוצאות רלוונטיות לשאלה שלך."
        else:
            # בניית קונטקסט מהקטעים הרלוונטיים
            context = "\n\n---\n\n".join([
                f"מקור: {Path(n.metadata.get('file_path', 'Unknown')).name}\n{n.text}"
                for n in relevant_nodes[:3]
            ])
            
            # בניית prompt ל-LLM
            prompt = f"""אתה עוזר מועיל שעונה על שאלות על בסיס המידע שניתן לך.

הנחיות חשובות:
- תן תשובה מדויקת, תמציתית וישירה לשאלה
- אם השאלה דורשת תשובה קצרה (כמו "מה הצבע?"), תן תשובה בכמה מילים בלבד
- אם השאלה מורכבת יותר, תן תשובה מפורטת אך תמציתית
- השתמש רק במידע מהקונטקסט שניתן
- אם המידע לא מופיע בקונטקסט, אמר זאת בבירור

קונטקסט:
{context}

שאלה: {message}

תשובה:"""
            
            # קבלת תשובה מה-LLM
            messages = [ChatMessage(role="user", content=prompt)]
            response = llm.chat(messages)
            answer = response.message.content.strip()
        
        # פורמט חדש של Gradio
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": answer})
        
        return "", history
    
    with gr.Blocks(title="RAG - מערכת חכמה") as demo:
        with gr.Column(elem_classes="hero-section"):
            gr.HTML("""
            <div class="animated-title">
                <h1>RAG</h1>
                <p class="subtitle">מערכת חיפוש חכמה לתיעוד</p>
            </div>
            """)
        
        with gr.Column(elem_classes="examples-section"):
            gr.HTML("""
            <div class="examples-grid">
                <div class="example-card">מה הצבע העיקרי שנבחר?</div>
                <div class="example-card">איזה database נבחר?</div>
                <div class="example-card">מה הכללים של UI?</div>
                <div class="example-card">איך מתקינים את המערכת?</div>
            </div>
            """)
        
        chatbot = gr.Chatbot(
            label="",
            height=450,
            rtl=True,
            elem_id="chatbot",
            show_label=False
        )
        
        with gr.Row(elem_classes="input-section"):
            msg = gr.Textbox(
                label="",
                placeholder="שאל שאלה...",
                scale=4,
                rtl=True,
                show_label=False,
                elem_classes="modern-input"
            )
            submit = gr.Button("שלח", scale=1, variant="primary", elem_classes="modern-button")
        
        gr.HTML("""
        <div class="footer">
            <div class="pulse-dot"></div>
            <span>מופעל על ידי AI</span>
        </div>
        """)
        
        msg.submit(chat, [msg, chatbot], [msg, chatbot])
        submit.click(chat, [msg, chatbot], [msg, chatbot])
    
    return demo

def main():
    print("="*60)
    print("RAG Demo - Simple Version (No Pinecone)")
    print("="*60 + "\n")
    
    # 1. טעינת מסמכים
    documents = load_documents()
    
    if not documents:
        print("\nError: No documents found!")
        return
    
    # 2. יצירת אינדקס
    index = create_index(documents)
    
    # 3. יצירת ממשק
    print("\n" + "="*60)
    print("Launching Gradio interface...")
    print("The interface will open at: http://127.0.0.1:7872")
    print("="*60 + "\n")
    
    demo = create_chat_interface(index)
    
    # CSS מודרני ומרהיב
    custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .gradio-container {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        min-height: 100vh;
    }
    
    /* Light Mode Container */
    .light .gradio-container {
        background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
    }
    
    .light .animated-title h1 {
        background: linear-gradient(135deg, #0099cc 0%, #00cc66 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .light .subtitle {
        color: #555;
    }
    
    .light .example-card {
        background: rgba(0, 0, 0, 0.03);
        border: 1px solid rgba(0, 212, 255, 0.3);
        color: #000;
    }
    
    .light .example-card:hover {
        background: rgba(0, 212, 255, 0.1);
    }
    
    .light .footer {
        color: #999;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
    }
    
    .animated-title h1 {
        font-size: 5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        animation: glow 2s ease-in-out infinite alternate;
        letter-spacing: -0.05em;
    }
    
    @keyframes glow {
        from {
            filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.5));
        }
        to {
            filter: drop-shadow(0 0 40px rgba(0, 255, 136, 0.8));
        }
    }
    
    .subtitle {
        color: #888;
        font-size: 1.2rem;
        font-weight: 300;
        margin-top: 0.5rem;
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Examples Grid */
    .examples-section {
        margin-bottom: 2rem;
    }
    
    .examples-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        padding: 0 2rem;
    }
    
    .example-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 212, 255, 0.2);
        padding: 1.2rem;
        border-radius: 12px;
        color: #fff;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        backdrop-filter: blur(10px);
    }
    
    .example-card:hover {
        background: rgba(0, 212, 255, 0.1);
        border-color: #00d4ff;
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
    }
    
    /* Chatbot */
    #chatbot {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin: 0 2rem 2rem 2rem;
    }
    
    /* Chatbot Messages - Dark Mode */
    .dark #chatbot .message,
    #chatbot .message {
        background: transparent !important;
        border: none !important;
    }
    
    /* User Messages */
    .dark #chatbot .message.user,
    #chatbot .message.user,
    .dark .user-message,
    .user-message {
        background: rgba(0, 212, 255, 0.15) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 16px 16px 4px 16px !important;
        padding: 1rem 1.2rem !important;
        color: #fff !important;
        margin: 0.5rem 0 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Bot Messages */
    .dark #chatbot .message.bot,
    #chatbot .message.bot,
    .dark .bot-message,
    .bot-message {
        background: rgba(0, 255, 136, 0.1) !important;
        border: 1px solid rgba(0, 255, 136, 0.2) !important;
        border-radius: 16px 16px 16px 4px !important;
        padding: 1rem 1.2rem !important;
        color: #fff !important;
        margin: 0.5rem 0 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Light Mode Support */
    .light #chatbot {
        background: rgba(0, 0, 0, 0.02) !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
    }
    
    .light .user-message {
        background: rgba(0, 212, 255, 0.1) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        color: #000 !important;
    }
    
    .light .bot-message {
        background: rgba(0, 255, 136, 0.1) !important;
        border: 1px solid rgba(0, 255, 136, 0.3) !important;
        color: #000 !important;
    }
    
    /* Message Text */
    #chatbot .message p,
    #chatbot .message-content {
        color: inherit !important;
        margin: 0 !important;
    }
    
    /* Input Section */
    .input-section {
        padding: 0 2rem 2rem 2rem;
        gap: 1rem;
    }
    
    .modern-input input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-size: 1rem !important;
        padding: 1.2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .modern-input input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    .modern-input input::placeholder {
        color: #666 !important;
    }
    
    /* Button */
    .modern-button {
        background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: #000 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 1.2rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4) !important;
    }
    
    .modern-button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(0, 255, 136, 0.6) !important;
    }
    
    .modern-button:active {
        transform: translateY(0) scale(0.98) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        padding: 2rem;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #00ff88;
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.5;
            transform: scale(1.2);
        }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%);
    }
    """
    
    demo.launch(share=False, server_name="127.0.0.1", server_port=7872, css=custom_css)

if __name__ == "__main__":
    main()
