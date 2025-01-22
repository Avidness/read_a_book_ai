from app.services.pinecone.ChapterAdapter import ChapterAdapter
from app.agents.BigPictureArchitect import BigPictureArchitect
from app.services.neo4j.CharacterGraph import CharacterGraph

async def generate_book(user_input: str):
  try:
      # Create an Outline
      agent = BigPictureArchitect(user_input)
      outline = await agent.generate_outline()
      yield outline.to_json()

      # Store Characters
      with CharacterGraph() as graph:
          for c in outline.characters:
            print(f"Adding character: {c.name}")
            graph.add_character(c)
            
      # Store Chapters
      adapter = ChapterAdapter()
      for chap in outline.chapters:
          existing_chapter = adapter.get_chapter_by_id(chap.chapter_id)
          if existing_chapter:
              adapter.update_chapter(chap)
          else:
              adapter.upsert_chapter(chap)
                  
  except Exception as e:
      yield f"Error running core pipeline: {e}"
