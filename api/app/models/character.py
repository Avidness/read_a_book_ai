from pydantic import BaseModel, Field, UUID4
import json
from uuid import uuid4

class Character(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    name: str
    arc: str
    physical_desc: str
    psychological_desc: str

    def to_json(self) -> str:
        return json.dumps(self.model_dump(exclude={"id"}))
