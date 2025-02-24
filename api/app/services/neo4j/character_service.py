from app.models.character_result import CharacterResult
from neo4j import RoutingControl
from typing import Optional, List, Dict, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.models.character import Character
from app.services.neo4j.connection import Neo4jConnection

class CharacterService:
    """Service for character-related database operations."""
    
    def __init__(self, connection: Neo4jConnection, embedding_model=None, similarity_threshold=0.85):
        """
        Initialize with a database connection.
        
        Args:
            connection: Neo4j database connection
            embedding_model: Model for generating embeddings from text
            similarity_threshold: Threshold for considering two entities as the same
        """
        self.connection = connection
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
    
    def generate_character_embedding(self, character: Character) -> Optional[np.ndarray]:
        """
        Generate an embedding for a character with emphasis on name and aliases.
        
        Args:
            character: Character to generate embedding for
            
        Returns:
            Embedding vector or None if no embedding model is available
        """
        if not self.embedding_model:
            return None
            
        # Create a brief description from character attributes
        description = ""
        if character.physical_desc:
            description += character.physical_desc + " "
        if character.psychological_desc:
            description += character.psychological_desc + " "
        if character.arc:
            description += character.arc
            
        # For characters with no embedding model, use the regular encode method
        if not hasattr(self.embedding_model, 'encode_entity'):
            full_text = f"{character.name} "
            if character.alt_names:
                full_text += " ".join(character.alt_names) + " "
            full_text += description
            return self.embedding_model.encode(full_text)
            
        # Generate embedding with weighted emphasis on names
        return self.embedding_model.encode_entity(
            name=character.name,
            alt_names=character.alt_names,
            description=description,
            weight_primary=3,  # Primary name gets highest weight
            weight_alt=2,      # Aliases get medium weight
            weight_desc=1      # Description gets lowest weight
        )
    
    def add_character(self, character: Character, embedding=None):
        """
        Add a character node to the graph with all their properties.
        
        Args:
            character: Character object to add
            embedding: Vector embedding of character's identifying features
        """
        # Ensure alt_names includes the character's primary name
        if character.alt_names is None:
            character.alt_names = [character.name]
        elif character.name not in character.alt_names:
            character.alt_names.append(character.name)
        
        # Generate embedding if not provided
        if embedding is None:
            embedding = self.generate_character_embedding(character)
        
        query = """
            MERGE (c:Character {name: $name})
            SET c.arc = $arc,
                c.physical_desc = $physical_desc,
                c.psychological_desc = $psychological_desc,
                c.alt_names = $alt_names
        """
        
        params = {
            "name": character.name,
            "arc": character.arc,
            "physical_desc": character.physical_desc,
            "psychological_desc": character.psychological_desc,
            "alt_names": character.alt_names
        }
        
        # Add embedding if available
        if embedding is not None:
            query += ", c.embedding = $embedding"
            params["embedding"] = embedding.tolist() if hasattr(embedding, "tolist") else embedding
            
        self.connection.driver.execute_query(
            query,
            params,
            database_=self.connection.db_name,
        )
    
    def get_character(self, name: str) -> Optional[CharacterResult]:
        """
        Retrieve a character by exact name match.
        
        Args:
            name: Character name to search for
            
        Returns:
            CharacterResult if found, None otherwise
        """
        records, _, _ = self.connection.driver.execute_query(
            """
            MATCH (c:Character {name: $name})
            RETURN c.name as name,
                   c.arc as arc,
                   c.physical_desc as physical_desc,
                   c.psychological_desc as psychological_desc,
                   c.embedding as embedding,
                   c.alt_names as alt_names
            """,
            name=name,
            database_=self.connection.db_name,
            routing_=RoutingControl.READ,
        )
        
        if not records:
            return None
            
        record = records[0]
        character = Character(
            name=record["name"],
            arc=record["arc"],
            physical_desc=record["physical_desc"],
            psychological_desc=record["psychological_desc"],
            alt_names=record["alt_names"]
        )
        
        return CharacterResult(
            character=character,
            embedding=record["embedding"]
        )
    
    def get_character_by_alias(self, alias: str) -> Optional[CharacterResult]:
        """
        Check if a character exists with the given alias in their alt_names.
        
        Args:
            alias: Alternative name to search for
            
        Returns:
            CharacterResult if found, None otherwise
        """
        records, _, _ = self.connection.driver.execute_query(
            """
            MATCH (c:Character)
            WHERE $alias IN c.alt_names
            RETURN c.name as name,
                   c.arc as arc,
                   c.physical_desc as physical_desc,
                   c.psychological_desc as psychological_desc,
                   c.embedding as embedding,
                   c.alt_names as alt_names
            LIMIT 1
            """,
            alias=alias,
            database_=self.connection.db_name,
            routing_=RoutingControl.READ,
        )
        
        if not records:
            return None
            
        record = records[0]
        character = Character(
            name=record["name"],
            arc=record["arc"],
            physical_desc=record["physical_desc"],
            psychological_desc=record["psychological_desc"],
            alt_names=record["alt_names"]
        )
        
        return CharacterResult(
            character=character,
            embedding=record["embedding"]
        )
    
    def get_all_characters(self) -> List[CharacterResult]:
        """
        Retrieve all characters with their embeddings.
        
        Returns:
            List of CharacterResult objects
        """
        records, _, _ = self.connection.driver.execute_query(
            """
            MATCH (c:Character)
            WHERE c.embedding IS NOT NULL
            RETURN c.name as name,
                   c.arc as arc,
                   c.physical_desc as physical_desc,
                   c.psychological_desc as psychological_desc,
                   c.embedding as embedding,
                   c.alt_names as alt_names
            """,
            database_=self.connection.db_name,
            routing_=RoutingControl.READ,
        )
        
        results = []
        for record in records:
            character = Character(
                name=record["name"],
                arc=record["arc"],
                physical_desc=record["physical_desc"],
                psychological_desc=record["psychological_desc"],
                alt_names=record["alt_names"]
            )
            
            results.append(CharacterResult(
                character=character,
                embedding=record["embedding"]
            ))
        return results
    
    def find_similar_character(self, character_desc: str = None, character: Character = None, embedding=None) -> Optional[CharacterResult]:
        """
        Find the most similar character based on embedding similarity.
        
        Args:
            character_desc: Textual description of the character (optional)
            character: Character object to match (optional)
            embedding: Pre-computed embedding vector (optional)
            
        Returns:
            CharacterResult with similarity score if found, None if no similar character is found
        """
        # Generate embedding if not provided
        if embedding is None:
            if character:
                embedding = self.generate_character_embedding(character)
            elif character_desc and self.embedding_model:
                # Just use standard encoding for text description
                embedding = self.embedding_model.encode(character_desc)
            else:
                return None  # Not enough information to generate embedding
        
        if embedding is None:
            return None
            
        # Get all characters with embeddings
        all_characters = self.get_all_characters()
        if not all_characters:
            return None
            
        # Calculate similarity with each character
        max_similarity = 0
        most_similar_character = None
        
        for char_result in all_characters:
            char_embedding = char_result.embedding
            if char_embedding:
                # Convert embeddings to numpy arrays if they aren't already
                query_embedding = np.array(embedding).reshape(1, -1)
                char_embedding = np.array(char_embedding).reshape(1, -1)
                
                # Calculate cosine similarity
                similarity = cosine_similarity(query_embedding, char_embedding)[0][0]
                
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_character = char_result
        
        # Return the most similar character if it exceeds the threshold
        if max_similarity >= self.similarity_threshold and most_similar_character:
            return CharacterResult(
                character=most_similar_character.character,
                embedding=most_similar_character.embedding,
                similarity=max_similarity
            )
            
        return None
    
    def consolidate_character(self, new_character: Character, existing_character_result: CharacterResult) -> CharacterResult:
        """
        Merge information from a new character into an existing one.
        
        Args:
            new_character: New character information
            existing_character_result: Existing character result
        
        Returns:
            Updated CharacterResult
        """
        existing_character = existing_character_result.character
        
        # Consolidate character information, prioritizing non-empty values
        consolidated_char = Character(
            name=existing_character.name,
            arc=new_character.arc if (new_character.arc and not existing_character.arc) else existing_character.arc,
            physical_desc=new_character.physical_desc if (new_character.physical_desc and not existing_character.physical_desc) else existing_character.physical_desc,
            psychological_desc=new_character.psychological_desc if (new_character.psychological_desc and not existing_character.psychological_desc) else existing_character.psychological_desc,
            alt_names=existing_character.alt_names or []
        )
        
        # Add the new character name as an alternative name if different
        if new_character.name != existing_character.name:
            consolidated_char.add_alt_name(new_character.name)
        
        # Add any new alternative names from the new character
        if new_character.alt_names:
            for alt_name in new_character.alt_names:
                consolidated_char.add_alt_name(alt_name)
        
        # Update the character in the database
        self.connection.driver.execute_query(
            """
            MATCH (c:Character {name: $name})
            SET c.arc = $arc,
                c.physical_desc = $physical_desc,
                c.psychological_desc = $psychological_desc,
                c.alt_names = $alt_names
            """,
            name=consolidated_char.name,
            arc=consolidated_char.arc,
            physical_desc=consolidated_char.physical_desc,
            psychological_desc=consolidated_char.psychological_desc,
            alt_names=consolidated_char.alt_names,
            database_=self.connection.db_name,
        )
        
        # Return updated result
        return CharacterResult(
            character=consolidated_char,
            embedding=existing_character_result.embedding
        )