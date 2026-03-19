from setuptools import setup, find_packages

setup(
    name="rag-agentic-docs",
    version="1.0.0",
    description="RAG system for Agentic Coding documentation",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "llama-index>=0.10.12",
        "llama-index-core>=0.10.12",
        "llama-index-llms-cohere>=0.1.3",
        "llama-index-embeddings-cohere>=0.1.6",
        "cohere>=5.0.4",
        "llama-index-vector-stores-pinecone>=0.1.3",
        "pinecone-client>=3.0.3",
        "gradio>=4.16.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.3",
        "pymongo>=4.6.1",
    ],
    python_requires=">=3.9",
)
