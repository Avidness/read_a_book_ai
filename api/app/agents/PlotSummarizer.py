from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class PlotSummarizer:
    def __init__(self, chapter_text, existing_summary=''):
        self.chapter_text = chapter_text
        self.existing_summary = existing_summary
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.llm = self.llm.bind(response_format={"type": "json_object"})

    async def generate_outline(self):
        prompt_template = PromptTemplate.from_file("app/prompts/summarize_plot.md")
        prompt = prompt_template.format(
            chapter_text=self.book_topic,
            existing_summary=self.existing_summary
        )
        response = await self.llm.ainvoke(prompt)
        return self.parse_response(response)