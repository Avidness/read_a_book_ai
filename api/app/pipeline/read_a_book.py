import json
from typing import List, Dict, Any, Generator, Optional
from app.agents.summary_extractor import SummaryExtractor
from app.utils.file_utils import chunkify_textblob
from app.services.neo4j.connection import Neo4jConnection
from app.services.neo4j.character_service import CharacterService, CharacterResult
from app.services.neo4j.location_service import LocationService, LocationResult
from app.services.neo4j.relationship_service import RelationshipService
from app.services.neo4j.embedding_service import EmbeddingService
from app.models.character import Character
from app.models.location import Location
from app.models.relationship import Relationship

async def process_book(result: Dict[str, Any]) -> Generator[str, None, None]:
    """
    Process a book by extracting entities and relationships using AI, 
    then store them in a Neo4j knowledge graph.
    
    Args:
        result: Dictionary containing processed book data
        
    Yields:
        Progress updates as strings
    """
    # Extract the text content from the result
    blob = result["processed_data"]["text_content"]
    
    # Split the text into manageable chunks
    chunks = chunkify_textblob(blob)
    yield f"Extracted file text -> Splitting into {len(chunks)} chunks"
    
    # Initialize embedding service for semantic entity matching
    embedding_service = EmbeddingService()
    
    # Initialize connection and services
    connection = Neo4jConnection(db_name="story_graph")
    character_service = CharacterService(connection, embedding_service)
    location_service = LocationService(connection, embedding_service)
    relationship_service = RelationshipService(connection)
    
    try:
        results = []
        
        # Process each chunk of the book
        for i, chunk in enumerate(chunks[:2]):  # Limited to first 2 chunks for testing
            yield f"Processing chunk {i+1}/{len(chunks[:2])}"
            
            # Extract entities and relationships from the chunk
            agent = SummaryExtractor(chunk)
            result_json = await agent.run()
            
            # Parse the extraction result
            parsed_result = json.loads(result_json)
            
            # Log extracted information
            yield f"Extracted {len(parsed_result['characters'])} characters, " \
                  f"{len(parsed_result['locations'])} locations, " \
                  f"{len(parsed_result['relationships'])} relationships"
            
            # Store the extraction in Neo4j, with automatic entity consolidation
            store_extraction_in_graph(
                character_service=character_service,
                location_service=location_service,
                relationship_service=relationship_service,
                extraction=parsed_result
            )
            
            results.append(result_json)
            
        # Retrieve consolidated entities count
        character_count = len(character_service.get_all_characters())
        location_count = len(location_service.get_all_locations())
        
        yield f"Book processed. Consolidated into {character_count} unique characters and {location_count} unique locations."
        yield json.dumps({
            "filename": "result.filename",
            "processed_data": result,
            "extraction_results": results
        })
    finally:
        # Ensure the connection is closed
        connection.close()

def find_matching_character(character_service: CharacterService, character: Character) -> Optional[CharacterResult]:
    """
    Find a matching character using multiple strategies.
    
    Args:
        character_service: CharacterService instance
        character: Character to match
        
    Returns:
        CharacterResult if a match is found, None otherwise
    """
    # Try exact name match
    result = character_service.get_character(character.name)
    if result:
        return result
    
    # Try alternative names
    result = character_service.get_character_by_alias(character.name)
    if result:
        return result
    
    # Try similar character using embedding
    # First check if there's enough data to do a meaningful comparison
    has_data = bool(character.physical_desc or character.psychological_desc or character.arc or character.alt_names)
    
    if has_data:
        # If we have some description or alt names, try similarity matching
        description = f"{character.name} "
        if character.physical_desc:
            description += character.physical_desc + " "
        if character.psychological_desc:
            description += character.psychological_desc + " "
        if character.arc:
            description += character.arc
            
        result = character_service.find_similar_character(character_desc=description)
        return result
    
    return None

def find_matching_location(location_service: LocationService, location: Location) -> Optional[LocationResult]:
    """
    Find a matching location using multiple strategies.
    
    Args:
        location_service: LocationService instance
        location: Location to match
        
    Returns:
        LocationResult if a match is found, None otherwise
    """
    # Try exact name match
    result = location_service.get_location(location.name)
    if result:
        return result
    
    # Try alternative names
    result = location_service.get_location_by_alias(location.name)
    if result:
        return result
    
    # Try similar location using embedding
    # First check if there's enough data to do a meaningful comparison
    has_data = bool(location.description or location.significance or location.alt_names)
    
    if has_data:
        # If we have some description or alt names, try similarity matching
        description = f"{location.name} "
        if location.description:
            description += location.description + " "
        if location.significance:
            description += location.significance
            
        result = location_service.find_similar_location(location_desc=description)
        return result
    
    return None

def store_extraction_in_graph(
    character_service: CharacterService,
    location_service: LocationService,
    relationship_service: RelationshipService,
    extraction: Dict[str, Any]
) -> None:
    """
    Store extracted entities and relationships in the Neo4j graph.
    
    Args:
        character_service: CharacterService instance
        location_service: LocationService instance
        relationship_service: RelationshipService instance
        extraction: Dictionary with extracted entities and relationships
    """
    # Store characters with their properties
    for char_data in extraction.get("characters", []):
        character = Character(
            name=char_data["name"],
            arc=char_data.get("arc", ""),
            physical_desc=char_data.get("physical_description", ""),
            psychological_desc=char_data.get("psychological_description", ""),
            alt_names=char_data.get("alt_names", [])
        )
        
        # Add character - entity consolidation happens automatically
        existing_result = find_matching_character(character_service, character)
        if existing_result:
            character_service.consolidate_character(character, existing_result)
        else:
            character_service.add_character(character)
    
    # Store locations with their properties
    for loc_data in extraction.get("locations", []):
        location = Location(
            name=loc_data["name"],
            description=loc_data.get("description", ""),
            significance=loc_data.get("significance", ""),
            alt_names=loc_data.get("alt_names", [])
        )
        
        # Add location - entity consolidation happens automatically
        existing_result = find_matching_location(location_service, location)
        if existing_result:
            location_service.consolidate_location(location, existing_result)
        else:
            location_service.add_location(location)
    
    # Store relationships between entities
    for rel_data in extraction.get("relationships", []):
        # Check for entity resolution in relationships
        source_name = rel_data["source"]
        target_name = rel_data["target"]
        
        # Try to find matching character for source
        if rel_data["type"] == "character_to_character" or rel_data["type"].startswith("character_to"):
            source_char = find_matching_character(
                character_service, 
                Character(name=source_name, arc="", physical_desc="", psychological_desc="")
            )
            if source_char:
                source_name = source_char.character.name
        
        # Try to find matching entity for target
        if rel_data["type"] == "character_to_character":
            target_char = find_matching_character(
                character_service,
                Character(name=target_name, arc="", physical_desc="", psychological_desc="")
            )
            if target_char:
                target_name = target_char.character.name
        elif rel_data["type"] == "character_to_location" or rel_data["type"].endswith("_to_location"):
            target_loc = find_matching_location(
                location_service,
                Location(name=target_name, description="", significance="")
            )
            if target_loc:
                target_name = target_loc.location.name
        
        # Create and add the relationship
        relationship = Relationship(
            source=source_name,
            target=target_name,
            type=rel_data["type"],
            properties=rel_data.get("properties", {}),
            description=rel_data.get("description", "")
        )
        relationship_service.add_relationship(relationship)