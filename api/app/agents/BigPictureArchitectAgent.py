from app.models.Chapter import Chapter
from app.models.Character import Character
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json

class BigPictureArchitectAgent:
    def __init__(self, book_topic):
        self.book_topic = book_topic
        load_dotenv()
        openai_key = os.getenv('OPENAI_API_KEY')
        os.environ["OPENAI_API_KEY"] = openai_key

        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        self.llm = self.llm.bind(response_format={"type": "json_object"})

    async def generate_outline(self):
        prompt = (
            f"You are an expert in creating book outlines. Create a comprehensive and detailed outline for a book on the following topic:\n"
            f"<START_TOPIC>{self.book_topic}<END_TOPIC>\n"
            f"The outline must return a JSON object with the following structure:\n"
            f"{{\n"
            f"  \"chapters\": [\n"
            f"    {{\"chapter_id\": 1, \"chapter_name\": \"name of the chapter\", \"chapter_summary\": \"description of what should happen in this chapter\"}}\n"
            f"  ],\n"
            f"  \"characters\": [\n"
            f"    {{\"character_name\": \"name of character\", \"arc\": \"description of the major plot points the character has through the book\", \"physical_desc\": \"a brief description of the character's physical appearance\", \"psychological_desc\": \"a breakdown of the character's psychological profile and personality type\"}}\n"
            f"  ]\n"
            f"}}"
        )

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