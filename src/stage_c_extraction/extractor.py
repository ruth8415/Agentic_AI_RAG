from typing import List, Dict
from llama_index.core import Document
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.llms.cohere import Cohere
from .schema import (
    Decision, Rule, Warning, Dependency, Change,
    SourceInfo, ExtractedItems, ExtractedDataSchema,
    ToolSource, FileSource
)
from datetime import datetime
from pathlib import Path
import hashlib
import config

class StructuredDataExtractor:
    def __init__(self):
        self.llm = Cohere(
            api_key=config.COHERE_API_KEY,
            model="command-r-plus"
        )
    
    def _create_extraction_program(self, output_cls):
        prompt_template = """
        You are an expert at extracting structured information from documentation.
        
        Extract relevant items from the following text. Be thorough and accurate.
        Only extract items that are explicitly mentioned or clearly implied.
        
        Text:
        {text}
        
        Extract all relevant items in the specified format.
        """
        
        return LLMTextCompletionProgram.from_defaults(
            output_cls=output_cls,
            prompt_template_str=prompt_template,
            llm=self.llm,
            verbose=False
        )
    
    def extract_decisions(self, documents: List[Document]) -> List[Decision]:
        decisions = []
        
        class DecisionList(BaseModel):
            items: List[Decision]
        
        program = self._create_extraction_program(DecisionList)
        
        for doc in documents:
            try:
                result = program(text=doc.text)
                
                for decision in result.items:
                    decision.source = SourceInfo(
                        tool=doc.metadata.get("tool", "Unknown"),
                        file=doc.metadata.get("relative_path", "Unknown")
                    )
                    decisions.append(decision)
            except Exception as e:
                print(f"Error extracting decisions from {doc.metadata.get('file_path')}: {e}")
        
        return decisions
    
    def extract_rules(self, documents: List[Document]) -> List[Rule]:
        rules = []
        
        class RuleList(BaseModel):
            items: List[Rule]
        
        program = self._create_extraction_program(RuleList)
        
        for doc in documents:
            try:
                result = program(text=doc.text)
                
                for rule in result.items:
                    rule.source = SourceInfo(
                        tool=doc.metadata.get("tool", "Unknown"),
                        file=doc.metadata.get("relative_path", "Unknown")
                    )
                    rules.append(rule)
            except Exception as e:
                print(f"Error extracting rules from {doc.metadata.get('file_path')}: {e}")
        
        return rules
    
    def extract_warnings(self, documents: List[Document]) -> List[Warning]:
        warnings = []
        
        class WarningList(BaseModel):
            items: List[Warning]
        
        program = self._create_extraction_program(WarningList)
        
        for doc in documents:
            try:
                result = program(text=doc.text)
                
                for warning in result.items:
                    warning.source = SourceInfo(
                        tool=doc.metadata.get("tool", "Unknown"),
                        file=doc.metadata.get("relative_path", "Unknown")
                    )
                    warnings.append(warning)
            except Exception as e:
                print(f"Error extracting warnings from {doc.metadata.get('file_path')}: {e}")
        
        return warnings
    
    def extract_all(self, documents: List[Document]) -> ExtractedDataSchema:
        print("Extracting structured data from documents...")
        
        print("  - Extracting decisions...")
        decisions = self.extract_decisions(documents[:5])
        
        print("  - Extracting rules...")
        rules = self.extract_rules(documents[:5])
        
        print("  - Extracting warnings...")
        warnings = self.extract_warnings(documents[:5])
        
        items = ExtractedItems(
            decisions=decisions,
            rules=rules,
            warnings=warnings
        )
        
        sources = self._build_sources(documents)
        
        schema = ExtractedDataSchema(
            sources=sources,
            items=items
        )
        
        print(f"\nExtracted: {len(decisions)} decisions, {len(rules)} rules, {len(warnings)} warnings")
        
        return schema
    
    def _build_sources(self, documents: List[Document]) -> List[ToolSource]:
        tools_map = {}
        
        for doc in documents:
            tool = doc.metadata.get("tool", "Unknown")
            file_path = doc.metadata.get("file_path", "")
            
            if tool not in tools_map:
                tools_map[tool] = {
                    "root_path": doc.metadata.get("source_dir", ""),
                    "files": {}
                }
            
            if file_path and file_path not in tools_map[tool]["files"]:
                try:
                    path_obj = Path(file_path)
                    if path_obj.exists():
                        stat = path_obj.stat()
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.sha256(f.read()).hexdigest()
                        
                        tools_map[tool]["files"][file_path] = FileSource(
                            path=file_path,
                            last_modified=datetime.fromtimestamp(stat.st_mtime),
                            hash=f"sha256:{file_hash[:16]}..."
                        )
                except Exception:
                    pass
        
        sources = []
        for tool, data in tools_map.items():
            sources.append(ToolSource(
                tool=tool,
                root_path=data["root_path"],
                files=list(data["files"].values())
            ))
        
        return sources

from pydantic import BaseModel
