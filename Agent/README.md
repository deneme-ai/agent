## UdaPlay Agent

UdaPlay is a research-style Q&A assistant for video games. It uses a local JSON dataset with RAG (ChromaDB) first, evaluates answer quality, and falls back to web search (Tavily) when needed. New facts learned from the web are stored back into ChromaDB.

### Project structure

```
udaplay-agent/
  games/              # JSON files used in Part 01
  chroma_db/
  lib/                # starter-style Agent + tooling
  notebooks/
    Udaplay_01_solution_project.ipynb
    Udaplay_02_solution_project.ipynb
```

### Quick start

1. Create a local `.env` file with your keys:

```
OPENAI_API_KEY="YOUR_KEY"
TAVILY_API_KEY="YOUR_KEY"
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the notebooks in `notebooks/` for the full pipeline demo.

### Notes

- If Tavily is not configured, the agent will skip web search.
- ChromaDB persists to `chroma_db/` by default.
