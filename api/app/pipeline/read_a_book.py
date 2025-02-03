import json
from app.agents.summary_extractor import SummaryExtractor
from app.utils.file_utils import chunkify_textblob
from app.services.neo4j.story_graph import StoryGraph

async def process_book(result: str):
    blob = result["processed_data"]["text_content"]
    
    chunks = chunkify_textblob(blob)

    yield "Extracted file text -> Splitting into chunks" + str(len(chunks))

    # store chunk in pinecone

    results = []
    for chunk in chunks[:1]:
        SummaryExtractor

        agent = SummaryExtractor(chunk)
        result = await agent.run()

        json_obj = json.loads(result)
        print(json_obj["themes"])
        print(json_obj["summary"])
        
        print(json_obj["locations"])
        print(json_obj["characters"])
        print(json_obj["relationships"])
        
        with StoryGraph() as graph:
            graph.parse_and_store_story_data(result)
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