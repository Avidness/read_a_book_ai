You are an expert in creating book outlines. Create a comprehensive and detailed outline for a book on the following topic:

<BOOK_TOPIC>{book_topic}</BOOK_TOPIC>

The outline must return a JSON object with the following structure:
<SAMPLE_RESPONSE_STRUCTURE>
{{
  "chapters": [
    {{
      {{
        "chapter_id": 1, 
        "chapter_name": "name of the chapter", 
        "chapter_summary": "description of what should happen in this chapter"
      }}
    }}
  ],
  "characters": [
    {{
      {{
        "character_name": "name of character", 
        "arc": "description of the major plot points the character has through the book", 
        "physical_desc": "a brief description of the character's physical appearance", 
        "psychological_desc": "a breakdown of the character's psychological profile and personality type"
      }}
    }}
  ]
}}
</SAMPLE_RESPONSE_STRUCTURE>