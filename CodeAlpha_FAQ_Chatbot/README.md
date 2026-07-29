# CodeAlpha_FAQChatbot

**CodeAlpha AI Internship — Task 2: Chatbot for FAQs**

🔗 **Live Demo:** https://codealphatasks-gy6utfuyh9ixgnzvoiabk6.streamlit.app

A Streamlit chatbot that answers user questions by matching them against a
set of FAQs using TF-IDF vectorization + cosine similarity.

## Features
- Chat-style UI (`st.chat_message` / `st.chat_input`)
- Text preprocessing (lowercasing, punctuation removal)
- TF-IDF + cosine similarity matching against FAQ questions
- Confidence threshold with a graceful fallback answer when no good match exists
- Sidebar listing all available FAQ topics
- Editable `faqs.json` — swap in your own product/topic FAQs easily

## Tech Stack
- Python
- Streamlit (UI)
- scikit-learn (TF-IDF + cosine similarity)

## Run Locally

```bash
git clone https://github.com/sachin8987-coder/codealpha_tasks.git
cd codealpha_tasks/CodeAlpha_FAQ_Chatbot
pip install -r requirements.txt
streamlit run app.py
```

App opens at `http://localhost:8501`.

## Customizing the FAQs
Edit `faqs.json` — it's a simple list of `{"question": ..., "answer": ...}`
objects. No retraining needed; the TF-IDF matrix rebuilds automatically
(cached with `@st.cache_resource`).

## 🚀 Deployment (Streamlit Community Cloud — Free)

This project lives inside the `codealpha_tasks` repo, alongside the other
CodeAlpha internship projects, as the `CodeAlpha_FAQ_Chatbot` subfolder.

1. **Push to GitHub** (already done — part of the shared `codealpha_tasks` repo)

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io and sign in with GitHub.
   - Click **"Create app"** → select repo `sachin8987-coder/codealpha_tasks`.
   - Branch: `main`
   - Main file path: `CodeAlpha_FAQ_Chatbot/app.py`
   - Click **Deploy**. Wait 1–2 minutes.
   - You'll get a public URL like the live demo link above.

3. **Verify**
   - Open the URL and test a few questions to confirm matching works live.

4. **Submit**
   - Record a short video explaining the project, post on LinkedIn tagging
     **@CodeAlpha**, and include the GitHub repo link.
   - Fill the CodeAlpha submission form with repo link + LinkedIn post link.

## Notes
- Threshold (`CONFIDENCE_THRESHOLD = 0.25`) controls when the bot admits it
  doesn't know an answer — tune it if you add more/less FAQs.
- For a larger FAQ set, consider swapping TF-IDF for sentence-transformers
  embeddings for better semantic matching (optional enhancement, not required).
