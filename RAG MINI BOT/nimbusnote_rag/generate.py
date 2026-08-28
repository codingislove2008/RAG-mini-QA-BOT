import os
import requests
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are a NimbusNote help bot.
Answer using ONLY the retrieved passages below.
If the passages do not contain the answer, say you do not see it in the NimbusNote docs.
Do not invent features, prices, or policies.
Keep the answer short (a few sentences). Mention the document name you used."""


def _format_context(hits: list[dict]) -> str:
    parts = []
    for i, h in enumerate(hits, start=1):
        parts.append(f"[{i}] {h['source']} — {h['section']}\n{h['text']}")
    return "\n\n".join(parts)


def answer_from_passages(question: str, hits: list[dict]) -> str:
    # fallback when no groq/openai key is provided
    if not hits:
        return (
            "I don't see that in the NimbusNote docs. "
            "Try asking about workspaces, sync, pricing, images, or troubleshooting."
        )

    best = hits[0]
    # strip first line if it just repeats the section title
    body = best["text"].split("\n", 1)[-1].strip() if "\n" in best["text"] else best["text"]
    lines = [
        body,
        "",
        f"Source: {best['source']} — {best['section']} (similarity {best['score']})",
    ]
    if len(hits) > 1:
        lines.append("Also retrieved:")
        for h in hits[1:]:
            lines.append(f"- {h['source']} / {h['section']} ({h['score']})")
    return "\n".join(lines)


def _call_llm(url: str, key: str, model: str, question: str, hits: list[dict]) -> str | None:
    if not key:
        return None
    try:
        res = requests.post(
            url,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "temperature": 0.1,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Passages:\n{_format_context(hits)}\n\nQuestion: {question}"},
                ],
            },
            timeout=30,
        )
        if res.status_code == 200:
            data = res.json()
            return data["choices"][0]["message"]["content"].strip()
    except requests.RequestException:
        # if api call times out or fails, just fallback to raw chunks
        return None
    return None


def generate_answer(question: str, hits: list[dict]) -> str:
    if not hits:
        return (
            "I don't see that in the NimbusNote docs. "
            "The retrieval step found no passage similar enough to your question."
        )

    groq_key = os.getenv("GROQ_API_KEY", "").strip()
    if groq_key:
        ans = _call_llm(
            "https://api.groq.com/openai/v1/chat/completions",
            groq_key,
            os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            question,
            hits,
        )
        if ans:
            return ans

    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key:
        ans = _call_llm(
            "https://api.openai.com/v1/chat/completions",
            openai_key,
            os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            question,
            hits,
        )
        if ans:
            return ans

    return answer_from_passages(question, hits)

