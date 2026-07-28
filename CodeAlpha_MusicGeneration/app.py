"""
CodeAlpha - Task 3: Music Generation with AI
app.py

Streamlit UI: click a button to generate a brand-new piece of music using
the trained LSTM model, preview a piano-roll style plot of the notes, and
download the result as a MIDI file.
"""

import io
import streamlit as st
import matplotlib.pyplot as plt

from generate import load_artifacts, generate_notes, tokens_to_midi

st.set_page_config(page_title="AI Music Generator", page_icon="🎵", layout="centered")

st.title("🎵 AI Music Generation")
st.caption("CodeAlpha AI Internship - Task 3 (LSTM trained on Bach chorales)")

st.markdown(
    "This app uses an **LSTM neural network** trained on Bach chorales "
    "(via `music21`'s bundled corpus) to compose new, original note "
    "sequences, then converts them into a downloadable **MIDI** file."
)


@st.cache_resource
def get_model_and_mappings():
    return load_artifacts()


model, mappings = get_model_and_mappings()

col1, col2 = st.columns(2)
with col1:
    num_notes = st.slider("Length (notes)", min_value=50, max_value=400, value=150, step=10)
with col2:
    temperature = st.slider(
        "Creativity (temperature)", min_value=0.3, max_value=1.5, value=0.8, step=0.1,
        help="Lower = safer/more repetitive, Higher = more random/experimental",
    )

instrument_choice = st.selectbox("Instrument", ["Piano", "Violin", "Flute", "Guitar"])

if "generated_tokens" not in st.session_state:
    st.session_state.generated_tokens = None
    st.session_state.midi_path = None

if st.button("🎼 Generate New Music", type="primary", use_container_width=True):
    with st.spinner("Composing... the LSTM is thinking in notes 🎹"):
        tokens = generate_notes(model, mappings, num_notes=num_notes, temperature=temperature)
        midi_path = tokens_to_midi(tokens, output_file="generated_music.mid", instrument_name=instrument_choice)
        st.session_state.generated_tokens = tokens
        st.session_state.midi_path = midi_path

if st.session_state.generated_tokens:
    st.success(f"Generated {len(st.session_state.generated_tokens)} notes/chords!")

    # Simple piano-roll style visualization
    fig, ax = plt.subplots(figsize=(10, 3))
    y_vals = []
    for tok in st.session_state.generated_tokens:
        if "." in tok:
            y_vals.append(int(tok.split(".")[0]))
        elif tok.isdigit():
            y_vals.append(int(tok))
        else:
            try:
                from music21 import note as m21note
                y_vals.append(m21note.Note(tok).pitch.midi)
            except Exception:
                y_vals.append(60)
    ax.plot(range(len(y_vals)), y_vals, marker="o", markersize=2, linewidth=1)
    ax.set_xlabel("Step")
    ax.set_ylabel("Pitch (MIDI number)")
    ax.set_title("Generated Melody Contour")
    st.pyplot(fig)

    with open(st.session_state.midi_path, "rb") as f:
        midi_bytes = f.read()

    st.download_button(
        label="⬇️ Download MIDI file",
        data=midi_bytes,
        file_name="ai_generated_music.mid",
        mime="audio/midi",
        use_container_width=True,
    )
    st.caption(
        "Open the downloaded .mid file in any DAW, MuseScore, VLC, or online "
        "MIDI player to listen to it."
    )

st.divider()
st.caption("Built with Streamlit + TensorFlow/Keras (LSTM) + music21")
