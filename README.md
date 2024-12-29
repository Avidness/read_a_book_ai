# Novel-AI

**🏗️ Work in Progress 🏗️**


The goal is to use AI to generate, manage, and proofread book-length content.

Separate agents need to coordinate together to ensure consistency with information that is outside their context window. Shared memory / history will be stored in a vector database.

---

## Tech Stack

- LangChain
- OpenAI
- Pinecone
- FastAPI
- React (CRA)

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