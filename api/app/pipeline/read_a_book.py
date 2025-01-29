import json
from app.agents.summary_extractor import SummaryExtractor
from app.utils.file_utils import chunkify_textblob

async def process_book(result: str):
    blob = result["processed_data"]["text_content"]
    
    chunks = chunkify_textblob(blob)

    yield "Extracted file text -> Splitting into chunks" + str(len(chunks))

    # store chunk in pinecone

    results = []
    for chunk in chunks[:2]:
        SummaryExtractor

        agent = SummaryExtractor(chunk)
        result = await agent.run()

        json_obj = json.loads(result)
        print(json_obj)
        print(json_obj.themes)
        print(json_obj.summary)
        
        print(json_obj.locations)
        print(json_obj.characters)
        print(json_obj.relationships)

        # extract characters, relationships, locations, themes
        # consolidate with existing characters, relationships, locations

        # Consolidate logic - 
        # search for name/alias results, 
        # if exists, 
        #   plug both versions into agent to rewrite a merged version 
        
        # store result in neo4j
        print(result)

        results.append(result)

    yield json.dumps({
        "filename": "result.filename",
        "processed_data": result
    })