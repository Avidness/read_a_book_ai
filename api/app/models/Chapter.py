
from pydantic import BaseModel
import json

class Chapter(BaseModel):
    chapter_id: int
    chapter_name: str
    chapter_summary: str

    def to_json(self) -> str:
        return json.dumps(self.dict())