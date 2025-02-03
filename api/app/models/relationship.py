from typing import Dict
import json
from uuid import uuid4
from pydantic import BaseModel, Field, UUID4

class Relationship(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    type: str
    description: str
    source: str
    target: str
    properties: Dict[str, str]

    def to_json(self) -> str:
        return json.dumps(self.dict())