from app.models.relationship import Relationship
from app.services.neo4j.connection import Neo4jConnection

class RelationshipService:
    """Service for relationship-related database operations."""
    
    def __init__(self, connection: Neo4jConnection):
        """
        Initialize with a database connection.
        
        Args:
            connection: Neo4j database connection
        """
        self.connection = connection
    
    def add_relationship(self, relationship: Relationship):
        """
        Add a relationship between two characters or a character and a location.
        
        Args:
            relationship: Relationship object to add
        """
        # Determine source and target node labels
        source_label = "Character" 
        target_label = "Character" if relationship.type == "character_to_character" else "Location"
        
        query = (
            f"MERGE (a:{source_label} {{name: $source_name}}) "
            f"MERGE (b:{target_label} {{name: $target_name}}) "
            f"MERGE (a)-[r:{relationship.type}]->(b) "
        )
        
        # Add properties if they exist
        if relationship.properties:
            set_clause = "SET " + ", ".join(f"r.{key} = ${key}" for key in relationship.properties.keys())
            query += set_clause

        params = {
            "source_name": relationship.source,
            "target_name": relationship.target,
            **relationship.properties
        }
        
        self.connection.driver.execute_query(
            query, 
            params, 
            database_=self.connection.db_name
        )