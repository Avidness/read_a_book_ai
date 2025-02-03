from neo4j import GraphDatabase, RoutingControl
from typing import Optional
from app.models.character import Character
from app.models.location import Location
from app.models.relationship import Relationship 
import json

class StoryGraph:
    def __init__(self, uri="bolt://neo4j:7687", auth=("neo4j", "password")):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        """Close the driver connection."""
        self.driver.close()

    # Character methods
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

    # Location methods
    def add_location(self, location: Location):
        """Add a location node to the graph with all its properties."""
        self.driver.execute_query(
            """
            MERGE (l:Location {name: $name})
            SET l.description = $description,
                l.significance = $significance
            """,
            name=location.name,
            description=location.description,
            significance=location.significance,
            database_="neo4j",
        )

    # Relationship methods
    def add_story_relationship(self, relationship: Relationship):
        """Add a relationship between two characters or a character and a location."""
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
        self.driver.execute_query(query, params, database_="neo4j")

    def get_location(self, name: str) -> Optional[Location]:
        """Retrieve a location by name."""
        records, _, _ = self.driver.execute_query(
            """
            MATCH (l:Location {name: $name})
            RETURN l.name as name,
                   l.description as description,
                   l.significance as significance
            """,
            name=name,
            database_="neo4j",
            routing_=RoutingControl.READ,
        )
        
        if not records:
            return None
            
        record = records[0]
        return Location(
            name=record["name"],
            description=record["description"],
            significance=record["significance"]
        )

    def parse_and_store_story_data(self, json_data: str):
        """Parse JSON data and store all entities in Neo4j."""
        data = json.loads(json_data)
        
        # Store characters
        for char_data in data["characters"]:
            character = Character(**char_data)
            self.add_character(character)
            
        # Store locations
        for loc_data in data["locations"]:
            location = Location(**loc_data)
            self.add_location(location)
            
        # Store relationships
        for rel_data in data["relationships"]:
            relationship = Relationship(**rel_data)
            self.add_story_relationship(relationship)

    def __enter__(self):
        """Enable usage with context manager."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the driver when exiting context manager."""
        self.close()