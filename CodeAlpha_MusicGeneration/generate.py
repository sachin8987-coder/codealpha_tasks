"""
CodeAlpha - Task 3: Music Generation with AI
generate.py

Loads the trained LSTM model and generates a brand-new note/chord sequence,
then converts it into a playable MIDI file using music21.

Can be run standalone:
    python generate.py
or imported by app.py for the Streamlit UI.
"""

import pickle
import random
import numpy as np
from music21 import stream, note, chord, instrument
from keras.models import load_model

import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(_BASE_DIR, "music_model.keras")
MAPPING_FILE = os.path.join(_BASE_DIR, "mappings.pkl")
DEFAULT_OUTPUT = os.path.join(_BASE_DIR, "generated_music.mid")


def load_artifacts():
    model = load_model(MODEL_FILE)
    with open(MAPPING_FILE, "rb") as f:
        mappings = pickle.load(f)
    return model, mappings


def generate_notes(model, mappings, num_notes=200, seed_sequence=None, temperature=1.0):
    """Generate a sequence of note/chord tokens using the trained LSTM."""
    note_to_int = mappings["note_to_int"]
    int_to_note = mappings["int_to_note"]
    n_vocab = mappings["n_vocab"]
    sequence_length = mappings["sequence_length"]

    if seed_sequence is None:
        start_keys = list(note_to_int.values())
        start = random.randint(0, max(0, len(start_keys) - sequence_length - 1))
        pattern = [start_keys[(start + i) % len(start_keys)] for i in range(sequence_length)]
    else:
        pattern = [note_to_int[n] for n in seed_sequence[-sequence_length:]]

    prediction_output = []

    for _ in range(num_notes):
        input_seq = np.reshape(pattern, (1, len(pattern), 1)) / float(n_vocab)
        prediction = model.predict(input_seq, verbose=0)[0]

        # temperature-based sampling for variety (1.0 = as trained, <1 more conservative, >1 more random)
        preds = np.log(np.clip(prediction, 1e-8, 1.0)) / max(temperature, 1e-3)
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        index = np.random.choice(range(n_vocab), p=preds)

        result = int_to_note[index]
        prediction_output.append(result)

        pattern.append(index)
        pattern = pattern[1:]

    return prediction_output


def tokens_to_midi(prediction_output, output_file=DEFAULT_OUTPUT, instrument_name="Piano"):
    """Convert a list of note/chord string tokens into a MIDI file."""
    offset = 0
    output_notes = []

    instrument_map = {
        "Piano": instrument.Piano,
        "Violin": instrument.Violin,
        "Flute": instrument.Flute,
        "Guitar": instrument.AcousticGuitar,
    }
    instr_cls = instrument_map.get(instrument_name, instrument.Piano)

    for pattern in prediction_output:
        if ("." in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split(".")
            chord_notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instr_cls()
                chord_notes.append(new_note)
            new_chord = chord.Chord(chord_notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instr_cls()
            output_notes.append(new_note)
        offset += 0.5

    midi_stream = stream.Stream(output_notes)
    midi_stream.write("midi", fp=output_file)
    return output_file


if __name__ == "__main__":
    model, mappings = load_artifacts()
    print("Generating new music sequence...")
    generated = generate_notes(model, mappings, num_notes=200)
    path = tokens_to_midi(generated)
    print(f"Saved generated music to {path}")
