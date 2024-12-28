import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

class SimpleQuestionService:
    def __init__(self, user_input):
        self.user_input = user_input
        load_dotenv()
        openai_key = os.getenv('OPENAI_API_KEY')
        os.environ["OPENAI_API_KEY"] = openai_key

        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.llm = self.llm.bind(response_format={"type": "json_object"})

    async def do_things(self):
        prompt = (
            f"You will think step-by-step and answer the following question: \n",
            f"{self.user_input}\n",
            f"All of your responses should be in JSON format.\n",
        )

        response = await self.llm.ainvoke(prompt)
        yield response.content
        