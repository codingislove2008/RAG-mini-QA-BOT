# NimbusNote RAG Mini Q&A Bot

A lightweight Retrieval-Augmented Generation (RAG) Q&A bot that answers questions about NimbusNote documentation using local embeddings and vector similarity search.

## Features

- **Local Vector Embeddings**: Uses `sentence-transformers` (`all-MiniLM-L6-v2`) locally — no paid embedding API required.
- **Smart Chunking**: Splits markdown documents by `##` headings for precise retrieval.
- **Cosine Similarity Search**: Ranks relevant passages in-memory using normalized dot-product search.
- **Flexible Generation**:
  - Works 100% offline without API keys (directly returns retrieved passages).
  - Optional integration with Groq or OpenAI for fluent answer synthesis.
- **Multiple Interfaces**: Streamlit Web UI and Terminal CLI.

## How to Run

### Quick Start
- **Windows**: Double-click **`start.bat`** (or run `.\start.bat` in terminal).
- **macOS / Linux**: Run `bash start.sh` (or `chmod +x start.sh && ./start.sh`).

The launcher script will automatically set up the virtual environment, install dependencies, and let you choose between the Web UI and CLI.

---

### Manual Setup
Requires **Python 3.10+**.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv

# On Windows:
.\.venv\Scripts\Activate.ps1
# On macOS / Linux:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the application
streamlit run app.py   # Web UI (http://localhost:8501)
# or:
python cli.py          # Terminal CLI
```

## Optional: LLM Configuration

The retrieval system works completely without an API key. If you want fluent AI-generated summaries, copy `.env.example` to `.env` and add a free [Groq API key](https://console.groq.com/keys) or OpenAI key:

```env
GROQ_API_KEY=your_groq_api_key_here
# or
OPENAI_API_KEY=your_openai_api_key_here
```

## Demo Questions

**In Documentation:**
- *How often does NimbusNote sync in the foreground?*
- *Can I attach images on the Free plan?*
- *What happens if two devices edit the same note?*
- *Is there a student discount on the Team plan?*
- *What does a red cloud icon mean?*

**Out of Scope (Correctly Refused):**
- *What is the capital of France?*
- *Does NimbusNote have a mobile dark mode?*

## Project Layout

| File / Folder | Description |
|---|---|
| `app.py` | Streamlit Web UI |
| `cli.py` | Terminal interactive chat interface |
| `docs/` | Knowledge base markdown documents |
| `nimbusnote_rag/load.py` | Document loading utility |
| `nimbusnote_rag/chunk.py` | Markdown section chunking logic |
| `nimbusnote_rag/embed.py` | Local sentence-transformer embeddings |
| `nimbusnote_rag/store.py` | In-memory vector store & cosine search |
| `nimbusnote_rag/generate.py` | Answer generation (with optional LLM) |
| `nimbusnote_rag/pipeline.py` | End-to-end retrieval & generation pipeline |
| `start.bat` / `start.sh` | One-click startup scripts for Windows, macOS, & Linux |

## MY HONEST REPLY

I want to be entirely honest regarding the work I've done. Since I'm a first-year s
tudent, I am still in the process of learning and discovering all sorts of new things 
each day. This program was made with the aid of various AI tools such as Antigravity, 
Cursor, and ChatGPT. I am not saying that I worked on it all by myself—I have used those 
tools in order to learn, to understand, to carry out experiments, and to turn my ideas 
into something practical.

In the future I intend to put in the necessary effort and keep on improving my abilities. 
Whenever you assign me an important project in the near future, I will treat it with 
seriousness, learn all that is needed, and do my best so as not to let you down.

I would also like to take a practical approach to my commitments, since I don’t want to 
join every club merely in order to have a long list of memberships and then not spend 
enough time on them. Instead, I prefer to concentrate on a small number of activities 
that are genuinely important for my development, for example MSA, Hack The Box, and 
GitHub, and to make a real contribution to these. My aim is to be honest about what I can 
commit to, to learn in a consistent way, and to demonstrate my abilities through my 
actual work rather than just through words.
