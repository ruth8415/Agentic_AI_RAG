from pathlib import Path
from src.stage_a_mvp.data_loader import AgenticDocsLoader
from src.stage_a_mvp.indexer import DocumentIndexer
from src.stage_a_mvp.query_engine import RAGQueryEngine
from src.stage_c_extraction.extractor import StructuredDataExtractor
from src.stage_c_extraction.storage import JSONStorage
from src.stage_c_extraction.router import HybridQueryRouter
from src.stage_c_extraction.gradio_app import GradioHybridInterface

def main():
    print("=== Stage C: Data Extraction & Hybrid Query System ===\n")
    
    project_path = Path(r"C:\Users\user1\Desktop\test_project")
    
    print(f"Using project path: {project_path}\n")
    
    print("1. Loading documents...")
    loader = AgenticDocsLoader(str(project_path))
    documents = loader.load_documents()
    
    if not documents:
        print("No documents found. Please check your project path.")
        return
    
    print("\n2. Creating vector index for semantic search...")
    indexer = DocumentIndexer()
    index = indexer.create_index(documents)
    
    print("\n3. Setting up semantic query engine...")
    semantic_engine = RAGQueryEngine(index, top_k=5)
    
    print("\n4. Extracting structured data...")
    extractor = StructuredDataExtractor()
    extracted_data = extractor.extract_all(documents)
    
    print("\n5. Saving extracted data...")
    storage = JSONStorage("extracted_data.json")
    storage.save(extracted_data)
    
    print("\n6. Setting up hybrid query router...")
    router = HybridQueryRouter(semantic_engine, storage_type="json")
    
    print("\n7. Launching Gradio interface...")
    print("\n" + "="*60)
    print("The interface will open at: http://127.0.0.1:7860")
    print("="*60 + "\n")
    
    app = GradioHybridInterface(router)
    app.launch(share=False, server_name="127.0.0.1", server_port=7860)

if __name__ == "__main__":
    main()
