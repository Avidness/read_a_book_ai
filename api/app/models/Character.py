from pydantic import BaseModel
import json

class Character(BaseModel):
    name: str
    arc: str
    physical_desc: str
    psychological_desc: str

    def to_json(self) -> str:
        return json.dumps(self.dict())