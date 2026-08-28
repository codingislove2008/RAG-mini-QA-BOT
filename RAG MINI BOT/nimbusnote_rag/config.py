from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# check docs/ first, with fallback to legacy task paths
DOC_LOCATIONS = [
    ROOT / "docs",
    ROOT / "recruit-task-rag-docs-main" / "recruit-task-rag-docs-main",
    ROOT / "recruit-task-rag-docs-main",
]
DOCS_DIR = next((p for p in DOC_LOCATIONS if p.exists()), ROOT / "docs")
CACHE_PATH = ROOT / ".cache" / "index.npz"

# lightweight local model from huggingface
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 3
MIN_SCORE = 0.28  # cutoff threshold to filter out unrelated questions

