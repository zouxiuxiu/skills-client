from typing import List, Optional
from pydantic import BaseModel

class SkillMetadata(BaseModel):
    name: str
    description: str
    version: str = "1.0.0"
    author: Optional[str] = None
    allowed_tools: List[str] = []

class Skill(BaseModel):
    metadata: SkillMetadata
    instructions: str   # Markdown body