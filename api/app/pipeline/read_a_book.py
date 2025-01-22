import json
'''
# Batch job to process bits at a time
# When AI finds a character, it will check the DB for an existing one and either update or create in neo4j
# Also keep track of relationships
# store each chunk in pinecone
# Retain chapter summaries
'''
async def process_book(result: str):
    print(result)
    yield json.dumps({
        "filename": "result.filename",
        "processed_data": "test"
    })