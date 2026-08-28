from nimbusnote_rag.pipeline import ask, get_store


def main() -> None:
    print("Loading NimbusNote document index...")
    store = get_store()
    print(f"Ready ({len(store.chunks)} chunks indexed). Ask a question, or type 'quit' to exit.\n")

    while True:
        try:
            q = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not q:
            continue
        if q.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        res = ask(q, store)
        print("\n--- Retrieved Passages ---")
        if not res["hits"]:
            print("  (no passages matched above similarity threshold)")
        for chunk in res["hits"]:
            print(f"  [{chunk['score']:.3f}] {chunk['source']} — {chunk['section']}")
        print(f"\nBot: {res['answer']}\n")


if __name__ == "__main__":
    main()

