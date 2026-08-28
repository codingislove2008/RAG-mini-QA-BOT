import re


def chunk_markdown(source: str, text: str) -> list[dict]:
    # split by markdown sections so chunks represent distinct topics
    raw = text.replace("\r\n", "\n").strip()
    if not raw:
        return []

    lines = raw.splitlines()
    doc_title = lines[0][2:].strip() if lines[0].startswith("# ") else "Document"

    # split at '## ' section headers
    sections = re.split(r"(?=\n## )", "\n" + raw)
    chunks = []

    for block in sections:
        block = block.strip()
        if not block:
            continue

        # skip lone top-level document headers
        if block.startswith("# ") and "\n## " not in block and len(block.splitlines()) == 1:
            continue

        block_lines = block.splitlines()
        first_line = block_lines[0]

        if first_line.startswith("## "):
            sec_name = first_line[3:].strip()
            body = "\n".join(block_lines[1:]).strip()
        elif first_line.startswith("# "):
            sec_name = doc_title
            body = "\n".join(block_lines[1:]).strip()
        else:
            sec_name = doc_title
            body = block

        if not body:
            continue

        chunks.append({
            "source": source,
            "section": sec_name,
            "text": f"{sec_name}\n{body}",
        })

    return chunks


def chunk_documents(documents: list[dict]) -> list[dict]:
    all_chunks = []
    for doc in documents:
        all_chunks.extend(chunk_markdown(doc["source"], doc["text"]))
    return all_chunks

