import os
from pathlib import Path
from typing import List, Dict
from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import Document
import config

class AgenticDocsLoader:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.tools_config = config.AGENTIC_TOOLS_CONFIG
    
    def find_tool_directories(self) -> Dict[str, List[Path]]:
        found_dirs = {}
        
        for tool_key, tool_info in self.tools_config.items():
            tool_paths = []
            for path_pattern in tool_info["paths"]:
                tool_dir = self.project_root / path_pattern
                if tool_dir.exists() and tool_dir.is_dir():
                    tool_paths.append(tool_dir)
            
            if tool_paths:
                found_dirs[tool_key] = tool_paths
        
        return found_dirs
    
    def load_documents(self) -> List[Document]:
        all_documents = []
        tool_dirs = self.find_tool_directories()
        
        if not tool_dirs:
            print(f"Warning: No agentic tool directories found in {self.project_root}")
            return all_documents
        
        for tool_key, paths in tool_dirs.items():
            tool_name = self.tools_config[tool_key]["name"]
            
            for tool_path in paths:
                try:
                    reader = SimpleDirectoryReader(
                        input_dir=str(tool_path),
                        required_exts=[".md"],
                        recursive=True,
                        exclude_hidden=False
                    )
                    
                    documents = reader.load_data()
                    
                    if not documents:
                        print(f"No .md files found in {tool_path}")
                        continue
                    
                    for doc in documents:
                        doc.metadata["tool"] = tool_name
                        doc.metadata["tool_key"] = tool_key
                        doc.metadata["source_dir"] = str(tool_path)
                        
                        relative_path = Path(doc.metadata.get("file_path", "")).relative_to(tool_path)
                        doc.metadata["relative_path"] = str(relative_path)
                    
                    all_documents.extend(documents)
                    print(f"Loaded {len(documents)} documents from {tool_name} ({tool_path})")
                
                except Exception as e:
                    print(f"Error loading from {tool_path}: {e}")
        
        print(f"\nTotal documents loaded: {len(all_documents)}")
        return all_documents
