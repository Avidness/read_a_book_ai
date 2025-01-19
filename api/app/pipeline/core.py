from app.agents.BigPictureArchitect import BigPictureArchitect
from app.services.neo4j.CharacterGraph import CharacterGraph

async def pipeline_core(user_input: str):
  #yield "Beginning request..."

  try:
      agent = BigPictureArchitect(user_input)
      outline = await agent.generate_outline()
      
      yield outline.to_json()

      with CharacterGraph() as graph:
          for c in outline.characters:
            
            print(f"Adding character: {c.name}")
            graph.add_character(c)
            
      '''
      for chap in outline.chapters:
        yield chap.to_json()

      for char in outline.characters:
        yield char.to_json()
      '''
  except Exception as e:
      yield f"Error running core pipeline: {e}"

  #async for result in await agent.generate_outline():
  #  yield result