# 📚 CorpusAI 🤖


**🏗️ Work in Progress 🏗️**

## Description:

### Case 1: Read a book
Take a large blob of text like a book and extract key elements:
* Themes
* Characters
* Character relationships
* Chapter Summaries

Store text blobs into Pinecone, Objects like Characters are stored in Neo4j.

Ask AI a questions and receive citations.

### Case 2: Write a book
Generate Characters and relationship graph (stored in Neo4j), write each chapter (stored in Pinecone).

### Case 3: Collaborative Writing

Start from a generated or existing book. Change characters, or writings, generate a new book based on your changes.


---

## Tech Stack

- LangChain
- OpenAI
- Pinecone
- Neo4j
- FastAPI
- React (Vite)

---

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/avidness/novel-ai.git
   ```

2. Navigate to the project directory:
   ```bash
   cd novel-ai
   ```

3. Start the services using Docker Compose:
   ```bash
   docker-compose up
   ```

---


## Features

### Agents
1. **Big Picture Architect**: 
   - Creates an outline of the chapters and characters in the book.

1. **Chapter Writer**:
   - Writes each chapter in a loop based on the outline.

1. **Summarize Chapter**:
   - Summarizes the previous chapter and passes the summary and outline to the next chapter for continuity.

1. **Proofreader**:
   - Proofreads each chapter for consistency and coherence.

1. **Consistency Checker**:
   - Searches the vector database for each theme and character to ensure consistency throughout the book.

---

## License
MIT