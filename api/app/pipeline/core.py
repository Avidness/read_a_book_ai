from app.services.SimpleQuestionService import SimpleQuestionService

async def pipeline_core(user_input: str):
  sqs = SimpleQuestionService(user_input)
  async for result in sqs.do_things():
    yield result