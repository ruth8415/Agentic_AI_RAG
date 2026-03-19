import sys
from pathlib import Path
from src.stage_a_mvp.data_loader import AgenticDocsLoader
from src.stage_a_mvp.indexer import DocumentIndexer
from src.stage_a_mvp.query_engine import RAGQueryEngine
from src.stage_a_mvp.gradio_app import GradioRAGInterface

def main():
    print("=== Stage A: MVP - RAG with Semantic Search ===\n")
    
    project_path = input("Enter the path to your project with agentic tools docs: ").strip()
    
    if not project_path:
        print("Error: Project path is required")
        return
    
    project_path = Path(project_path)
    if not project_path.exists():
        print(f"Error: Path {project_path} does not exist")
        return
    
    print("\n1. Loading documents...")
    loader = AgenticDocsLoader(str(project_path))
    documents = loader.load_documents()
    
    if not documents:
        print("No documents found. Please check your project path and ensure it contains agentic tool directories.")
        return
    
    print("\n2. Creating index and embeddings...")
    indexer = DocumentIndexer()
    index = indexer.create_index(documents)
    
    print("\n3. Setting up query engine...")
    query_engine = RAGQueryEngine(index, top_k=5)
    
    print("\n4. Launching Gradio interface...")
    app = GradioRAGInterface(query_engine)
    app.launch(share=False, server_name="127.0.0.1", server_port=7860)

if __name__ == "__main__":
    main()
