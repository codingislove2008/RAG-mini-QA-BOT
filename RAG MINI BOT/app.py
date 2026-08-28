import streamlit as st

from nimbusnote_rag.pipeline import ask, get_store

st.set_page_config(page_title="NimbusNote RAG Bot", page_icon="📓", layout="wide")
st.title("NimbusNote Q&A (RAG)")
st.caption("Retrieval-Augmented Q&A powered by local embeddings and vector similarity search.")


@st.cache_resource(show_spinner="Loading document index...")
def load_index():
    return get_store()


store = load_index()

if "history" not in st.session_state:
    st.session_state.history = []

user_query = st.chat_input("Ask about NimbusNote (syncing, pricing, plans, troubleshooting...)")

if user_query:
    res = ask(user_query, store)
    st.session_state.history.append(res)

chat_col, context_col = st.columns([1.3, 1])

with chat_col:
    if not st.session_state.history:
        st.info("💡 Try asking: *'How often does NimbusNote sync?'* or *'Is there a student discount on the Team plan?'*")
    for chat in st.session_state.history:
        with st.chat_message("user"):
            st.write(chat["question"])
        with st.chat_message("assistant"):
            st.write(chat["answer"])

with context_col:
    st.subheader("Retrieved passages")
    if not st.session_state.history:
        st.write("Submit a question to see the matching document passages retrieved from the index.")
    else:
        latest = st.session_state.history[-1]
        if not latest["hits"]:
            st.warning("No passage scored above the similarity threshold for this query.")
        for chunk in latest["hits"]:
            with st.expander(f"{chunk['source']} — {chunk['section']}  (score: {chunk['score']:.3f})", expanded=True):
                st.write(chunk["text"])

