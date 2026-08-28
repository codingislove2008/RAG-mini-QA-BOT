# Quick test to verify document loading and markdown chunking
from nimbusnote_rag.chunk import chunk_documents
from nimbusnote_rag.load import load_documents


def test_chunking() -> None:
    docs = load_documents()
    chunks = chunk_documents(docs)

    assert len(docs) == 3, f"Expected 3 docs, found {len(docs)}"
    assert len(chunks) >= 12, f"Expected at least 12 chunks, got {len(chunks)}"

    sources = {c["source"] for c in chunks}
    expected_sources = {
        "01-getting-started.md",
        "02-pricing-and-plans.md",
        "03-troubleshooting.md",
    }
    assert sources == expected_sources, f"Source mismatch: {sources}"

    sections = {c["section"] for c in chunks}
    assert "Free plan" in sections
    assert "Offline mode" in sections
    assert "Account recovery" in sections

    print(f"Verified: {len(docs)} documents parsed into {len(chunks)} chunks.")
    for c in chunks:
        print(f"  [{c['source']:24}] -> {c['section']}")


if __name__ == "__main__":
    test_chunking()

