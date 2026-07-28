"""
CodeAlpha - Task 1: Language Translation Tool
A Streamlit web app that translates text between languages using
the free Google Translate backend (via deep-translator), with an
optional text-to-speech (TTS) playback of the translated text.
"""

import streamlit as st
from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
from gtts import gTTS
import io

st.set_page_config(page_title="Language Translation Tool", page_icon="🌐", layout="centered")

st.title("🌐 Language Translation Tool")
st.caption("CodeAlpha AI Internship - Task 1")

# Build language options: "English (en)" -> "en"
LANG_OPTIONS = {f"{name.title()} ({code})": code for name, code in GOOGLE_LANGUAGES_TO_CODES.items()}
LANG_NAMES = sorted(LANG_OPTIONS.keys())

# Session state for translated text (so copy/TTS work after translation)
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

col1, col2 = st.columns(2)
with col1:
    source_lang_name = st.selectbox(
        "Source Language",
        ["Auto Detect"] + LANG_NAMES,
        index=0,
    )
with col2:
    default_target_index = LANG_NAMES.index("Hindi (hi)") + 1 if "Hindi (hi)" in LANG_NAMES else 1
    target_lang_name = st.selectbox(
        "Target Language",
        LANG_NAMES,
        index=LANG_NAMES.index("Hindi (hi)") if "Hindi (hi)" in LANG_NAMES else 0,
    )

input_text = st.text_area("Enter text to translate", height=150, placeholder="Type or paste text here...")

translate_clicked = st.button("Translate", type="primary", use_container_width=True)

if translate_clicked:
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        try:
            source_code = "auto" if source_lang_name == "Auto Detect" else LANG_OPTIONS[source_lang_name]
            target_code = LANG_OPTIONS[target_lang_name]

            translated = GoogleTranslator(source=source_code, target=target_code).translate(input_text)
            st.session_state.translated_text = translated
        except Exception as e:
            st.error(f"Translation failed: {e}")

if st.session_state.translated_text:
    st.subheader("Translated Text")
    st.text_area("Result", value=st.session_state.translated_text, height=150, key="result_box")

    col_a, col_b = st.columns(2)

    with col_a:
        st.code(st.session_state.translated_text, language=None)
        st.caption("👆 Use the copy icon on the box above to copy the translation.")

    with col_b:
        if st.button("🔊 Listen (Text-to-Speech)", use_container_width=True):
            try:
                target_code = LANG_OPTIONS[target_lang_name]
                tts = gTTS(text=st.session_state.translated_text, lang=target_code)
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format="audio/mp3")
            except Exception as e:
                st.error(f"Text-to-speech failed for this language: {e}")

st.divider()
st.caption("Built with Streamlit + deep-translator (Google Translate backend) + gTTS")
