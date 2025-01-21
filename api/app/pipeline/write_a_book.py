from app.services.pinecone.ChapterAdapter import ChapterAdapter
from app.agents.BigPictureArchitect import BigPictureArchitect
from app.services.neo4j.CharacterGraph import CharacterGraph

async def run(user_input: str):
  #yield "Beginning request..."

  try:
      agent = BigPictureArchitect(user_input)
      outline = await agent.generate_outline()
      
      yield outline.to_json()

      with CharacterGraph() as graph:
          for c in outline.characters:
            print(f"Adding character: {c.name}")
            graph.add_character(c)
            
      print('adapter')
      adapter = ChapterAdapter()
      print('adapter2')
      
      for chap in outline.chapters:
          print('Chapter', chap)
          existing_chapter = adapter.get_chapter_by_id(chap.chapter_id)
          if existing_chapter:
              adapter.update_chapter(chap)
              print('Chapter updated', chap)
          else:
              adapter.upsert_chapter(chap)
              print('Chapter created', chap)
                  
            

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