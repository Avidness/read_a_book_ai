import json
from uuid import uuid4
from pydantic import BaseModel, Field, UUID4

class Location(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    name: str
    description: str
    significance: str

    def to_json(self) -> str:
        return json.dumps(self.dict())