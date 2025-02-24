from app.models.location import Location

class LocationResult:
    """Contains a location with its embedding and metadata."""
    
    def __init__(self, location: Location, embedding=None, similarity=None):
        self.location = location
        self.embedding = embedding
        self.similarity = similarity