You are extracting important information from BOOK_TEXT which is a chunk of data from a larger book.

Respond with a JSON object that contains the following fields:
{{
    "themes": [],
    "characters: [],
    "locations": [],
    "relationships": [],
    "summary": "A summary of the events in this chunk of text"
}}

Use the following pydantic models define how you return the JSON objects for characters, locations and relationships. A character should have a relationship with a location if they are there, if they have been there, or if they might be going there in the future. Make note in the relationship properties if they live there, and other relevent details. Relationships can be between a character and another character, or a character and a location.

For characters, if a physical_desc isn't provided, include details like their age, gender, demeanor, clothing, etc.

Be explit about relationships, and include anything relevant, such as family relations and friendships.

class Character(BaseModel):
    name: str
    arc: str
    physical_desc: str
    psychological_desc: str

class Location(BaseModel):
    name: str
    description: str
    significance: str

class Relationship(BaseModel):
    type: str # character_to_character or character_to_location
    description: str
    source: str
    target: str
    properties: Dict[str, str] # key must not include spaces, but value can be full sentence, for example ["initial_impression", "Unimpressed by their attempts to charm."]

<BOOK_TEXT>{book_text}</BOOK_TEXT>