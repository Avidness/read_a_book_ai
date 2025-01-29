You are extracting important information from BOOK_TEXT which is a chunk of data from a larger book.

Respond with a JSON object that contains the following fields:
{{
    "themes": [],
    "characters: [],
    "locations": [],
    "relationships": [],
    "summary": "A summary of the events in this chunk of text"
}}

Use the following pydantic models define how you return the JSON objects for characters, locations and relationships. A character should have a relationship with a location if they are there, if they have been there, or if they might be going there in the future. Make note in the relationship properties if they live there, and other relevent details. If a physical_desc isn't provided, include details like their age, gender, demeanor, clothing, etc.

class Character(BaseModel):
    name: str
    arc: str
    physical_desc: str
    psychological_desc: str

class Location(BaseModel):
    name: str
    properties: Dict[str, str]

class Relationship(BaseModel):
    type: str
    source: str
    target: str
    properties: Dict[str, str]

<BOOK_TEXT>{book_text}</BOOK_TEXT>