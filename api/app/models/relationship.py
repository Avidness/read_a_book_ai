from typing import Dict
from pydantic import BaseModel
import json

class Relationship(BaseModel):
    type: str
    source_character: str
    target_character: str
    properties: Dict[str, str]

    def to_json(self) -> str:
        return json.dumps(self.dict())