# CodeAlpha_FAQChatbot

**CodeAlpha AI Internship — Task 2: Chatbot for FAQs**

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
git clone https://github.com/<your-username>/CodeAlpha_FAQChatbot.git
cd CodeAlpha_FAQChatbot
pip install -r requirements.txt
streamlit run app.py
```

App opens at `http://localhost:8501`.

## Customizing the FAQs
Edit `faqs.json` — it's a simple list of `{"question": ..., "answer": ...}`
objects. No retraining needed; the TF-IDF matrix rebuilds automatically
(cached with `@st.cache_resource`).

## 🚀 Deployment (Streamlit Community Cloud — Free)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Task 2: FAQ Chatbot"
   git branch -M main
   git remote add origin https://github.com/<your-username>/CodeAlpha_FAQChatbot.git
   git push -u origin main
   ```
   Repo name **must** be `CodeAlpha_FAQChatbot` (per internship naming rule:
   `CodeAlpha_ProjectName`).

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io and sign in with GitHub.
   - Click **"Create app"** → **"From existing repo"**.
   - Select the repo, branch `main`, main file path `app.py`.
   - Click **Deploy**. Wait 1–2 minutes.
   - You'll get a public URL like `https://codealpha-faqchatbot-yourname.streamlit.app`.

3. **Verify**
   - Open the URL and test a few questions to confirm matching works live.

4. **Submit**
   - Add the live URL + a screenshot to `README.md`.
   - Record a short video explaining the project, post on LinkedIn tagging
     **@CodeAlpha**, and include the GitHub repo link.
   - Fill the CodeAlpha submission form with repo link + LinkedIn post link.

## Notes
- Threshold (`CONFIDENCE_THRESHOLD = 0.25`) controls when the bot admits it
  doesn't know an answer — tune it if you add more/less FAQs.
- For a larger FAQ set, consider swapping TF-IDF for sentence-transformers
  embeddings for better semantic matching (optional enhancement, not required).
