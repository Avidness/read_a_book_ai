from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class ChapterWriter:
    def __init__(self, book_topic, characters, plot_summary, chapter_details):
        self.book_topic = book_topic
        self.characters = characters
        self.plot_summary = plot_summary
        self.chapter_details = chapter_details
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.llm = self.llm.bind(response_format={"type": "json_object"})

    async def run(self):
        prompt_template = PromptTemplate.from_file("app/prompts/write_chapter.md")
        prompt = prompt_template.format(
            book_topic=self.book_topic, 
            characters=self.characters, 
            plot_summary=self.plot_summary, 
            chapter_details=self.chapter_details
        )
        response = await self.llm.ainvoke(prompt)
        return response.content