from app.models.Chapter import Chapter
from app.models.Character import Character
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import json

class BigPictureArchitectAgent:
    def __init__(self, book_topic):
        self.book_topic = book_topic
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.llm = self.llm.bind(response_format={"type": "json_object"})

    async def generate_outline(self):
        prompt_template = PromptTemplate.from_file("app/prompts/generate_characters_and_chapters.md")
        prompt = prompt_template.format(book_topic=self.book_topic)

        response = await self.llm.ainvoke(prompt)
        outline_data = json.loads(response.content)
        chapters = outline_data.get("chapters", [])

        chapters = [
            Chapter(chapter_id=chapter["chapter_id"], chapter_name=chapter["chapter_name"], chapter_summary=chapter["chapter_summary"])
            for chapter in outline_data.get("chapters", [])
        ]

        characters = [
            Character(
                character_name=character["character_name"],
                arc=character["arc"],
                physical_desc=character["physical_desc"],
                psychological_desc=character["psychological_desc"]
            )
            for character in outline_data.get("characters", [])
        ]

        return {"chapters": chapters, "characters": characters}