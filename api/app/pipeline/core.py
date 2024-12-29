from app.agents.SimpleQuestionAgent import SimpleQuestionAgent

async def pipeline_core(user_input: str):
  agent = SimpleQuestionAgent(user_input)
  async for result in agent.do_things():
    yield result