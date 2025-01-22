You are extracting important information from BOOK_TEXT which is a chunk of data from a larger book.

Respond with a JSON object that contains the following fields, when relevant:

{{
    "themes": [],
    "characters: [],
    "locations": [],
    "summary": "A summary of the events in this chunk of text"
}}

<BOOK_TEXT>{book_text}</BOOK_TEXT>