from app.models.chapter import Chapter
from app.models.character import Character
from app.models.outline import Outline
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import json

class BigPictureArchitect:
    def __init__(self, book_topic):
        self.book_topic = book_topic
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.llm = self.llm.bind(response_format={"type": "json_object"})

    def parse_response(self, response) -> Outline:
            json_resp = json.loads(response.content)

            chapters = [
                Chapter(
                    chapter_id=chapter["chapter_id"], 
                    chapter_name=chapter["chapter_name"], 
                    chapter_summary=chapter["chapter_summary"]
                )
                for chapter in json_resp.get("chapters", [])
            ]

            characters = [
                Character(
                    name=character["name"],
                    arc=character["arc"],
                    physical_desc=character["physical_desc"],
                    psychological_desc=character["psychological_desc"]
                )
                for character in json_resp.get("characters", [])
            ]

            return Outline(book_topic=self.book_topic, chapters=chapters, characters=characters)
        
    async def generate_outline(self):
        prompt_template = PromptTemplate.from_file("app/prompts/generate_characters_and_chapters.md")
        prompt = prompt_template.format(book_topic=self.book_topic)
        response = await self.llm.ainvoke(prompt)
        return self.parse_response(response)