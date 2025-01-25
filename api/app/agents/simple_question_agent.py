from app.db.pinecone_adapter import PineconeAdapter
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

class SimpleQuestionAgent:
    def __init__(self, user_input):
        self.user_input = user_input
        load_dotenv()
        openai_key = os.getenv('OPENAI_API_KEY')
        os.environ["OPENAI_API_KEY"] = openai_key

        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.llm = self.llm.bind(response_format={"type": "json_object"})

    async def do_things(self):
        
        # Query pinecone first
        adapter = PineconeAdapter()
        results = adapter.query_index(self.user_input)
        print(results)

        prompt = (
            f"You will think step-by-step and answer the following question: \n",
            f"<START_QUESTION>{self.user_input}<END_QUESTION>\n",
            f"Respond only using the results from below:\n",
            f"<START_RESULTS>{results}<END_RESULTS>\n",
            f"All of your responses should be in JSON format.\n",
        )

        response = await self.llm.ainvoke(prompt)
        yield response.content
        