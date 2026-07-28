# CodeAlpha_MusicGeneration

**CodeAlpha AI Internship — Task 3: Music Generation with AI**

An LSTM neural network trained on Bach chorales (using `music21`'s bundled
corpus — no external MIDI download needed) that composes new, original
music. A Streamlit UI lets you generate a fresh piece on demand and download
it as a MIDI file.

## How it works
1. **`prepare_data.py`** — parses 40 Bach chorales bundled with `music21` and
   extracts a flat list of note/chord tokens.
2. **`train.py`** — builds a 2-layer LSTM (128 units each) with dropout,
   trains it to predict the next note/chord given the previous 20, and saves
   the trained model + vocabulary mappings.
3. **`generate.py`** — loads the trained model, seeds it with a starting
   pattern, and autoregressively samples a brand-new sequence (with a
   "temperature" control for creativity), then converts it into a real
   MIDI file using `music21`.
4. **`app.py`** — Streamlit UI: pick length / creativity / instrument, hit
   Generate, see a melody-contour plot, and download the `.mid` file.

The trained model (`music_model.keras`) and vocabulary (`mappings.pkl`) are
included in this folder, so the app works immediately — no training needed
before deploying.

## Tech Stack
- Python
- TensorFlow / Keras (LSTM)
- music21 (MIDI parsing/generation, bundled Bach corpus)
- Streamlit (UI)
- Matplotlib (melody visualization)

## Run Locally

```bash
cd CodeAlpha_MusicGeneration
pip install -r requirements.txt
streamlit run app.py
```

To retrain from scratch (optional):
```bash
python prepare_data.py   # extracts notes_data.pkl
python train.py          # trains and saves music_model.keras + mappings.pkl
```

## 🚀 Deployment — Single Repo, Multiple Project Subfolders

This project lives inside the shared **`codealpha_tasks`** repo, alongside
your other CodeAlpha projects (one subfolder per task).

### 1. Add this folder to your existing local repo
Copy the `CodeAlpha_MusicGeneration` folder into your local `codealpha_tasks`
folder (the same one that already has `CodeAlpha_Chatbot`,
`CodeAlpha_Hangman`, etc.), so it sits next to them:

```
codealpha_tasks/
    CodeAlpha_Chatbot/
    CodeAlpha_Hangman/
    CodeAlpha_IRIS_Flower_Classification/
    CodeAlpha_MusicGeneration/   <-- new
    README.md
```

### 2. Commit and push
```bash
cd codealpha_tasks
git add CodeAlpha_MusicGeneration
git commit -m "Added Music Generation with AI project"
git push
```
(If it's your first push, use `git init`, `git remote add origin <your-repo-url>`,
`git branch -M main`, `git push -u origin main` instead.)

### 3. Deploy the Streamlit app
Streamlit Cloud deploys **one app per main file**, so for a multi-project
repo you point it at this project's `app.py` specifically:

1. Go to https://share.streamlit.io → sign in with GitHub.
2. Click **"Create app"** → **"From existing repo"**.
3. Repository: `<your-username>/codealpha_tasks`
4. Branch: `main`
5. **Main file path: `CodeAlpha_MusicGeneration/app.py`** (this is the key
   step for a subfolder project — Streamlit needs the full path, not just
   `app.py`).
6. Click **Deploy**. First build may take a couple of minutes (TensorFlow is
   a larger dependency).
7. You'll get a live URL like `https://codealpha-music-yourname.streamlit.app`.

### 4. Verify & Submit
- Open the live URL, click "Generate New Music", download the `.mid`, and
  play it in any MIDI player (VLC, MuseScore, Windows Media Player) to
  confirm it sounds musical (not random noise).
- Record a short video explaining the project, post it on LinkedIn tagging
  **@CodeAlpha** with the repo link.
- Submit the repo link + LinkedIn post link via the WhatsApp submission form.

## Notes
- Training uses only 40 chorales / 40 epochs to keep things fast for a demo —
  more chorales + more epochs (100+) will produce noticeably more
  Bach-like, coherent music, at the cost of longer training time.
- The "temperature" slider in the app controls how safe vs. experimental the
  generated melody is — lower values sound closer to the training data,
  higher values are more surprising (and sometimes less musical).
