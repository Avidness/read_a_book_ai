from app.models.location_result import LocationResult
from neo4j import RoutingControl
from typing import Optional, List, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.models.location import Location
from app.services.neo4j.connection import Neo4jConnection

class LocationService:
    """Service for location-related database operations."""
    
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

    def generate_location_embedding(self, location: Location) -> Optional[np.ndarray]:
        """
        Generate an embedding for a location with emphasis on name and aliases.
        
        Args:
            location: Location to generate embedding for
            
        Returns:
            Embedding vector or None if no embedding model is available
        """
        if not self.embedding_model:
            return None
            
        # Create a brief description from location attributes
        description = ""
        if location.description:
            description += location.description + " "
        if location.significance:
            description += location.significance
            
        # For locations with no embedding model with encode_entity, use the regular encode method
        if not hasattr(self.embedding_model, 'encode_entity'):
            full_text = f"{location.name} "
            if location.alt_names:
                full_text += " ".join(location.alt_names) + " "
            full_text += description
            return self.embedding_model.encode(full_text)
            
        # Generate embedding with weighted emphasis on names
        return self.embedding_model.encode_entity(
            name=location.name,
            alt_names=location.alt_names,
            description=description,
            weight_primary=3,  # Primary name gets highest weight
            weight_alt=2,      # Aliases get medium weight
            weight_desc=1      # Description gets lowest weight
        )
    
    def add_location(self, location: Location, embedding=None):
        """
        Add a location node to the graph with all its properties.
        
        Args:
            location: Location object to add
            embedding: Vector embedding of location's identifying features
        """
        # Ensure alt_names includes the location's primary name
        if location.alt_names is None:
            location.alt_names = [location.name]
        elif location.name not in location.alt_names:
            location.alt_names.append(location.name)
        
        # Generate embedding if not provided
        if embedding is None:
            embedding = self.generate_location_embedding(location)
        
        query = """
            MERGE (l:Location {name: $name})
            SET l.description = $description,
                l.significance = $significance,
                l.alt_names = $alt_names
        """
        
        params = {
            "name": location.name,
            "description": location.description,
            "significance": location.significance,
            "alt_names": location.alt_names
        }
        
        # Add embedding if available
        if embedding is not None:
            query += ", l.embedding = $embedding"
            params["embedding"] = embedding.tolist() if hasattr(embedding, "tolist") else embedding
            
        self.connection.driver.execute_query(
            query,
            params,
            database_=self.connection.db_name,
        )
    
    def get_location(self, name: str) -> Optional[LocationResult]:
        """
        Retrieve a location by exact name match.
        
        Args:
            name: Location name to search for
            
        Returns:
            LocationResult if found, None otherwise
        """
        records, _, _ = self.connection.driver.execute_query(
            """
            MATCH (l:Location {name: $name})
            RETURN l.name as name,
                   l.description as description,
                   l.significance as significance,
                   l.embedding as embedding,
                   l.alt_names as alt_names
            """,
            name=name,
            database_=self.connection.db_name,
            routing_=RoutingControl.READ,
        )
        
        if not records:
            return None
            
        record = records[0]
        location = Location(
            name=record["name"],
            description=record["description"],
            significance=record["significance"],
            alt_names=record["alt_names"]
        )
        
        return LocationResult(
            location=location,
            embedding=record["embedding"]
        )
    
    def get_location_by_alias(self, alias: str) -> Optional[LocationResult]:
        """
        Check if a location exists with the given alias in their alt_names.
        
        Args:
            alias: Alternative name to search for
            
        Returns:
            LocationResult if found, None otherwise
        """
        records, _, _ = self.connection.driver.execute_query(
            """
            MATCH (l:Location)
            WHERE $alias IN l.alt_names
            RETURN l.name as name,
                   l.description as description,
                   l.significance as significance,
                   l.embedding as embedding,
                   l.alt_names as alt_names
            LIMIT 1
            """,
            alias=alias,
            database_=self.connection.db_name,
            routing_=RoutingControl.READ,
        )
        
        if not records:
            return None
            
        record = records[0]
        location = Location(
            name=record["name"],
            description=record["description"],
            significance=record["significance"],
            alt_names=record["alt_names"]
        )
        
        return LocationResult(
            location=location,
            embedding=record["embedding"]
        )
    
    def get_all_locations(self) -> List[LocationResult]:
        """
        Retrieve all locations with their embeddings.
        
        Returns:
            List of LocationResult objects
        """
        records, _, _ = self.connection.driver.execute_query(
            """
            MATCH (l:Location)
            WHERE l.embedding IS NOT NULL
            RETURN l.name as name,
                   l.description as description,
                   l.significance as significance,
                   l.embedding as embedding,
                   l.alt_names as alt_names
            """,
            database_=self.connection.db_name,
            routing_=RoutingControl.READ,
        )
        
        results = []
        for record in records:
            location = Location(
                name=record["name"],
                description=record["description"],
                significance=record["significance"],
                alt_names=record["alt_names"]
            )
            
            results.append(LocationResult(
                location=location,
                embedding=record["embedding"]
            ))
        return results
    
    def find_similar_location(self, location_desc: str = None, location: Location = None, embedding=None) -> Optional[LocationResult]:
        """
        Find the most similar location based on embedding similarity.
        
        Args:
            location_desc: Textual description of the location (optional)
            location: Location object to match (optional)
            embedding: Pre-computed embedding vector (optional)
            
        Returns:
            LocationResult with similarity score if found, None if no similar location is found
        """
        # Generate embedding if not provided
        if embedding is None:
            if location:
                embedding = self.generate_location_embedding(location)
            elif location_desc and self.embedding_model:
                # Just use standard encoding for text description
                embedding = self.embedding_model.encode(location_desc)
            else:
                return None  # Not enough information to generate embedding
        
        if embedding is None:
            return None
            
        # Get all locations with embeddings
        all_locations = self.get_all_locations()
        if not all_locations:
            return None
            
        # Calculate similarity with each location
        max_similarity = 0
        most_similar_location = None
        
        for loc_result in all_locations:
            loc_embedding = loc_result.embedding
            if loc_embedding:
                # Convert embeddings to numpy arrays if they aren't already
                query_embedding = np.array(embedding).reshape(1, -1)
                loc_embedding = np.array(loc_embedding).reshape(1, -1)
                
                # Calculate cosine similarity
                similarity = cosine_similarity(query_embedding, loc_embedding)[0][0]
                
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_location = loc_result
        
        # Return the most similar location if it exceeds the threshold
        if max_similarity >= self.similarity_threshold and most_similar_location:
            return LocationResult(
                location=most_similar_location.location,
                embedding=most_similar_location.embedding,
                similarity=max_similarity
            )
            
        return None
        
    def consolidate_location(self, new_location: Location, existing_location_result: LocationResult) -> LocationResult:
        """
        Merge information from a new location into an existing one.
        
        Args:
            new_location: New location information
            existing_location_result: Existing location result
        
        Returns:
            Updated LocationResult
        """
        existing_location = existing_location_result.location
        
        # Consolidate location information, prioritizing non-empty values
        consolidated_loc = Location(
            name=existing_location.name,
            description=new_location.description if (new_location.description and not existing_location.description) else existing_location.description,
            significance=new_location.significance if (new_location.significance and not existing_location.significance) else existing_location.significance,
            alt_names=existing_location.alt_names or []
        )
        
        # Add the new location name as an alternative name if different
        if new_location.name != existing_location.name:
            consolidated_loc.add_alt_name(new_location.name)
        
        # Add any new alternative names from the new location
        if new_location.alt_names:
            for alt_name in new_location.alt_names:
                consolidated_loc.add_alt_name(alt_name)
        
        # Update the location in the database
        self.connection.driver.execute_query(
            """
            MATCH (l:Location {name: $name})
            SET l.description = $description,
                l.significance = $significance,
                l.alt_names = $alt_names
            """,
            name=consolidated_loc.name,
            description=consolidated_loc.description,
            significance=consolidated_loc.significance,
            alt_names=consolidated_loc.alt_names,
            database_=self.connection.db_name,
        )
        
        # Return updated result
        return LocationResult(
            location=consolidated_loc,
            embedding=existing_location_result.embedding
        )