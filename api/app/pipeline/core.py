from app.agents.BigPictureArchitectAgent import BigPictureArchitectAgent

async def pipeline_core(user_input: str):
  agent = BigPictureArchitectAgent(user_input)
  result = await agent.generate_outline()
  print(result)
  
  for chap in result['chapters']:
    yield chap.to_json()

  for char in result['characters']:
    yield char.to_json()
    
  #async for result in await agent.generate_outline():
  #  yield result