from neo4j import GraphDatabase, RoutingControl
from typing import List, Optional
from app.models.character import Character

class CharacterGraph:
    def __init__(self, uri="bolt://neo4j:7687", auth=("neo4j", "password")):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        """Close the driver connection."""
        self.driver.close()

    def add_character(self, character: Character):
        """Add a character node to the graph with all their properties."""
        self.driver.execute_query(
            """
            MERGE (c:Character {name: $name})
            SET c.arc = $arc,
                c.physical_desc = $physical_desc,
                c.psychological_desc = $psychological_desc
            """,
            name=character.name,
            arc=character.arc,
            physical_desc=character.physical_desc,
            psychological_desc=character.psychological_desc,
            database_="neo4j",
        )

    def add_relationship(self, char1_name: str, char2_name: str, relationship_type: str, properties: Optional[dict] = None):
        """Add a relationship between two characters with optional properties."""
        if properties is None:
            properties = {}

        query = (
            "MERGE (a:Character {name: $char1_name}) "
            "MERGE (b:Character {name: $char2_name}) "
            f"MERGE (a)-[r:{relationship_type}]->(b) "
        )
        
        # Add properties
        if properties:
            set_clause = "SET " + ", ".join(f"r.{key} = ${key}" for key in properties.keys())
            query += set_clause

        params = {
            "char1_name": char1_name,
            "char2_name": char2_name,
            **properties
        }
        self.driver.execute_query(query, params, database_="neo4j")

    def get_character(self, name: str) -> Optional[Character]:
        """Retrieve a character by name."""
        records, _, _ = self.driver.execute_query(
            """
            MATCH (c:Character {name: $name})
            RETURN c.name as name,
                   c.arc as arc,
                   c.physical_desc as physical_desc,
                   c.psychological_desc as psychological_desc
            """,
            name=name,
            database_="neo4j",
            routing_=RoutingControl.READ,
        )
        
        if not records:
            return None
            
        record = records[0]
        return Character(
            name=record["name"],
            arc=record["arc"],
            physical_desc=record["physical_desc"],
            psychological_desc=record["psychological_desc"]
        )

    def get_relationships(self, char_name: str, relationship_type: Optional[str] = None) -> List[dict]:
        """Get all relationships of a character, optionally filtered by type."""
        query = """
            MATCH (a:Character {name: $name})-[r]->(b:Character)
            """
        if relationship_type:
            query += f"WHERE type(r) = $rel_type "
            
        query += """
            RETURN type(r) as relationship_type,
                   b.name as related_character,
                   properties(r) as properties
            """
        
        params = {"name": char_name}
        if relationship_type:
            params["rel_type"] = relationship_type
            
        records, _, _ = self.driver.execute_query(
            query,
            params,
            database_="neo4j",
            routing_=RoutingControl.READ,
        )
        
        return [
            {
                "type": record["relationship_type"],
                "character": record["related_character"],
                "properties": record["properties"]
            }
            for record in records
        ]

    def delete_character(self, name: str):
        """Delete a character and all their relationships."""
        self.driver.execute_query(
            """
            MATCH (c:Character {name: $name})
            DETACH DELETE c
            """,
            name=name,
            database_="neo4j",
        )

    def __enter__(self):
        """Enable usage with context manager."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the driver when exiting context manager."""
        self.close()
