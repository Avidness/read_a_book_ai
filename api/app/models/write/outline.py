from typing import List
from app.models.write.chapter import Chapter
from app.models.shared.character import Character
from pydantic import BaseModel
import json

class Outline(BaseModel):
    book_topic: str
    chapters: List[Chapter]
    characters: List[Character]

    def to_json(self) -> str:
        return json.dumps(self.dict())