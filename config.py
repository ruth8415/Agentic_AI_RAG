import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "agentic-coding-docs")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "rag_extracted_data")

AGENTIC_TOOLS_CONFIG = {
    "cursor": {
        "name": "Cursor",
        "paths": [".cursor", ".cursorrules"]
    },
    "windsurf": {
        "name": "Windsurf",
        "paths": [".windsurf"]
    },
    "claude": {
        "name": "Claude Code",
        "paths": [".claude"]
    }
}

CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
