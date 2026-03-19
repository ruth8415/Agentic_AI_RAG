from pathlib import Path
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.llms.cohere import Cohere
from src.stage_a_mvp.data_loader import AgenticDocsLoader
from src.stage_a_mvp.indexer import DocumentIndexer
from src.stage_b_event_driven.workflow_engine import WorkflowEngine
from src.stage_b_event_driven.gradio_app import GradioEventDrivenInterface
import config

def main():
    print("=== Stage B: Event-Driven Workflow ===\n")
    
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
        print("No documents found. Please check your project path.")
        return
    
    print("\n2. Creating index and embeddings...")
    indexer = DocumentIndexer()
    index = indexer.create_index(documents)
    
    print("\n3. Setting up workflow engine...")
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=5
    )
    
    llm = Cohere(
        api_key=config.COHERE_API_KEY,
        model="command-r-plus"
    )
    
    response_synthesizer = get_response_synthesizer(
        llm=llm,
        response_mode="compact"
    )
    
    workflow_engine = WorkflowEngine(retriever, response_synthesizer)
    
    print("\n4. Launching Gradio interface...")
    app = GradioEventDrivenInterface(workflow_engine)
    app.launch(share=False, server_name="127.0.0.1", server_port=7860)

if __name__ == "__main__":
    main()
