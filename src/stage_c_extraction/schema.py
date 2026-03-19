from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ItemType(str, Enum):
    DECISION = "decision"
    RULE = "rule"
    WARNING = "warning"
    DEPENDENCY = "dependency"
    CHANGE = "change"

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SourceInfo(BaseModel):
    tool: str = Field(description="The agentic tool name (e.g., Cursor, Windsurf)")
    file: str = Field(description="File path relative to tool directory")
    anchor: Optional[str] = Field(default=None, description="Section anchor or heading")
    line_range: Optional[List[int]] = Field(default=None, description="[start_line, end_line]")

class Decision(BaseModel):
    id: str
    title: str = Field(description="Short title of the decision")
    summary: str = Field(description="Brief summary of what was decided")
    tags: List[str] = Field(default_factory=list, description="Related tags")
    source: SourceInfo
    observed_at: datetime = Field(default_factory=datetime.now)

class Rule(BaseModel):
    id: str
    rule: str = Field(description="The rule or guideline text")
    scope: str = Field(description="Where this rule applies (e.g., ui, backend, db)")
    notes: Optional[str] = Field(default=None, description="Additional context")
    source: SourceInfo
    observed_at: datetime = Field(default_factory=datetime.now)

class Warning(BaseModel):
    id: str
    area: str = Field(description="Which area/component this warning relates to")
    message: str = Field(description="The warning message")
    severity: Severity = Field(default=Severity.MEDIUM)
    source: SourceInfo
    observed_at: datetime = Field(default_factory=datetime.now)

class Dependency(BaseModel):
    id: str
    name: str = Field(description="Dependency name")
    version: Optional[str] = Field(default=None, description="Version if specified")
    purpose: str = Field(description="Why this dependency is used")
    source: SourceInfo
    observed_at: datetime = Field(default_factory=datetime.now)

class Change(BaseModel):
    id: str
    title: str = Field(description="What changed")
    description: str = Field(description="Details of the change")
    impact: str = Field(description="Impact of this change")
    tags: List[str] = Field(default_factory=list)
    source: SourceInfo
    observed_at: datetime = Field(default_factory=datetime.now)

class ExtractedItems(BaseModel):
    decisions: List[Decision] = Field(default_factory=list)
    rules: List[Rule] = Field(default_factory=list)
    warnings: List[Warning] = Field(default_factory=list)
    dependencies: List[Dependency] = Field(default_factory=list)
    changes: List[Change] = Field(default_factory=list)

class FileSource(BaseModel):
    path: str
    last_modified: datetime
    hash: str

class ToolSource(BaseModel):
    tool: str
    root_path: str
    files: List[FileSource]

class ExtractedDataSchema(BaseModel):
    schema_version: str = "1.0"
    generated_at: datetime = Field(default_factory=datetime.now)
    sources: List[ToolSource] = Field(default_factory=list)
    items: ExtractedItems = Field(default_factory=ExtractedItems)
