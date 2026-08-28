from pathlib import Path

from .config import DOCS_DIR


def load_documents(docs_dir: Path | None = None) -> list[dict]:
    target_dir = docs_dir or DOCS_DIR
    if not target_dir.exists():
        raise FileNotFoundError(
            f"Docs directory not found: {target_dir}\n"
            "Make sure markdown docs are located in 'docs/' or 'recruit-task-rag-docs-main/'."
        )

    docs = []
    for fpath in sorted(target_dir.glob("*.md")):
        if fpath.name.lower() == "readme.md":
            continue
        try:
            content = fpath.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = fpath.read_text(encoding="latin-1")
            
        docs.append({"source": fpath.name, "text": content})

    if not docs:
        raise FileNotFoundError(f"No markdown documents (.md) found in {target_dir}")

    return docs

