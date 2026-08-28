from .chunk import chunk_documents
from .config import CACHE_PATH, DOCS_DIR
from .generate import generate_answer
from .load import load_documents
from .store import VectorStore, build_store


def get_store(rebuild: bool = False) -> VectorStore:
    if CACHE_PATH.exists() and not rebuild:
        return VectorStore.load()

    docs = load_documents(DOCS_DIR)
    chunks = chunk_documents(docs)
    store = build_store(chunks)
    store.save()
    return store


def ask(question: str, store: VectorStore | None = None) -> dict:
    q = question.strip()
    if not q:
        return {"question": question, "hits": [], "answer": "Please ask a question about NimbusNote."}

    vstore = store or get_store()
    hits = vstore.search(q)
    ans = generate_answer(q, hits)
    return {"question": q, "hits": hits, "answer": ans}

