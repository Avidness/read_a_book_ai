from app.models.character import Character

class CharacterResult:
    """Contains a character with its embedding and metadata."""
    
    def __init__(self, character: Character, embedding=None, similarity=None):
        self.character = character
        self.embedding = embedding
        self.similarity = similarity