from typing import List
from app.models.Chapter import Chapter
from app.models.Character import Character
from pydantic import BaseModel

class Outline(BaseModel):
    chapters: List[Chapter]
    characters: List[Character]