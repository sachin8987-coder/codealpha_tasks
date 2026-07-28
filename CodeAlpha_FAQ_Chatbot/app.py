"""
CodeAlpha - Task 2: Chatbot for FAQs
A Streamlit chatbot that matches a user's question against a set of
FAQs using TF-IDF vectorization + cosine similarity, and replies
with the best-matching answer.
"""

import json
import re
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="FAQ Chatbot", page_icon="💬", layout="centered")

st.title("💬 FAQ Chatbot")
st.caption("CodeAlpha AI Internship - Task 2")


@st.cache_resource
def load_faqs(path="faqs.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    questions = [item["question"] for item in data]
    answers = [item["answer"] for item in data]
    return questions, answers


def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


@st.cache_resource
def build_vectorizer(questions):
    processed = [preprocess(q) for q in questions]
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(processed)
    return vectorizer, matrix


questions, answers = load_faqs()
vectorizer, question_matrix = build_vectorizer(questions)

CONFIDENCE_THRESHOLD = 0.25  # below this, we admit we don't know
FALLBACK_ANSWER = (
    "Sorry, I couldn't find a confident match for that in my FAQ list. "
    "Try rephrasing your question, or ask about the internship, tasks, "
    "certificate, or submission process."
)


def get_best_answer(user_query: str):
    processed_query = preprocess(user_query)
    query_vec = vectorizer.transform([processed_query])
    similarities = cosine_similarity(query_vec, question_matrix)[0]
    best_idx = similarities.argmax()
    best_score = similarities[best_idx]
    if best_score < CONFIDENCE_THRESHOLD:
        return FALLBACK_ANSWER, best_score, None
    return answers[best_idx], best_score, questions[best_idx]


# --- Chat UI ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me anything about the CodeAlpha internship. 👋"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    answer, score, matched_q = get_best_answer(user_input)

    with st.chat_message("assistant"):
        st.markdown(answer)
        if matched_q:
            st.caption(f"Matched FAQ: \"{matched_q}\" (similarity: {score:.2f})")

    st.session_state.messages.append({"role": "assistant", "content": answer})

with st.sidebar:
    st.subheader("📋 Available FAQ topics")
    for q in questions:
        st.markdown(f"- {q}")
    st.divider()
    if st.button("Clear chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! Ask me anything about the CodeAlpha internship. 👋"}
        ]
        st.rerun()
