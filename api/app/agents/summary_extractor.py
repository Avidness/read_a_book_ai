from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class SummaryExtractor:
    def __init__(self, chunk):
        self.chunk = chunk
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.llm = self.llm.bind(response_format={"type": "json_object"})

    async def run(self):
        prompt_template = PromptTemplate.from_file("app/prompts/generate_summary.md")
        prompt = prompt_template.format(
            book_text=self.chunk,
        )
        response = await self.llm.ainvoke(prompt)
        return response.content