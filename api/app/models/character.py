from pydantic import BaseModel, Field, UUID4
import json
from uuid import uuid4
from typing import List, Optional

class Character(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    name: str
    arc: str
    physical_desc: str
    psychological_desc: str
    alt_names: Optional[List[str]] = Field(default=None)
    
    def to_json(self) -> str:
        return json.dumps(self.model_dump(exclude={"id"}))
    
    def add_alt_name(self, alt_name: str) -> None:
        """Add an alternative name if it doesn't already exist."""
        if alt_name == self.name:
            return
            
        if self.alt_names is None:
            self.alt_names = []
            
        if alt_name not in self.alt_names:
            self.alt_names.append(alt_name)