import json
from app.agents.summary_extractor import SummaryExtractor
from app.utils.file_utils import chunkify_textblob

async def process_book(result: str):
    blob = result["processed_data"]["text_content"]
    
    chunks = chunkify_textblob(blob)

    yield "Extracted file text -> Splitting into chunks" + str(len(chunks))

    results = []
    for chunk in chunks[:2]:
        SummaryExtractor

        agent = SummaryExtractor(chunk)
        result = await agent.run()
        print(result)
        results.append(result)

    yield json.dumps({
        "filename": "result.filename",
        "processed_data": chunks
    })