# CodeAlpha_LanguageTranslationTool

**CodeAlpha AI Internship — Task 1: Language Translation Tool**

A Streamlit web app that translates text between 100+ languages using the free
Google Translate backend (`deep-translator`), with optional text-to-speech
playback of the translation.

## Features
- Text input box + Source/Target language dropdowns (100+ languages)
- Auto-detect source language option
- Instant translation on button click
- Copy-friendly output box
- 🔊 Text-to-speech playback of the translated text (gTTS)

## Tech Stack
- Python
- Streamlit (UI)
- deep-translator (Google Translate backend, no API key needed)
- gTTS (text-to-speech)

## Run Locally

```bash
git clone https://github.com/<your-username>/CodeAlpha_LanguageTranslationTool.git
cd CodeAlpha_LanguageTranslationTool
pip install -r requirements.txt
streamlit run app.py
```

App opens at `http://localhost:8501`.

## 🚀 Deployment (Streamlit Community Cloud — Free)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Task 1: Language Translation Tool"
   git branch -M main
   git remote add origin https://github.com/<your-username>/CodeAlpha_LanguageTranslationTool.git
   git push -u origin main
   ```
   Repo name **must** be `CodeAlpha_LanguageTranslationTool` (per internship rules).

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io and sign in with GitHub.
   - Click **"Create app"** → **"From existing repo"**.
   - Select your repo, branch `main`, and main file path `app.py`.
   - Click **Deploy**. Wait 1–2 minutes for the build.
   - You'll get a live public URL like `https://codealpha-translation-yourname.streamlit.app`.

3. **Verify**
   - Open the URL, test a translation, confirm it works publicly (not just localhost).

4. **Submit**
   - Add the live URL + a screenshot/GIF to your `README.md`.
   - Push your source code to GitHub (already done in step 1).
   - Record a short screen-recording explaining the project, post it on LinkedIn
     tagging **@CodeAlpha**, and include the GitHub repo link.
   - Fill the CodeAlpha submission form with the repo link + LinkedIn post link.

## Notes
- No paid API key required — uses the free Google Translate web endpoint via
  `deep-translator`. For production/commercial use, consider the official
  Google Cloud Translation API instead.
- If gTTS fails for a language, that language may not support TTS — translation
  itself still works.
