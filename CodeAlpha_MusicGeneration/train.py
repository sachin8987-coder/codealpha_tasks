"""
CodeAlpha - Task 3: Music Generation with AI
train.py

Trains an LSTM model on the note/chord sequences prepared by prepare_data.py,
to learn musical patterns and later generate new sequences.

Run after prepare_data.py:
    python train.py
"""

import pickle
import numpy as np
from tensorflow import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Activation
from keras.utils import to_categorical

SEQUENCE_LENGTH = 20
NOTES_FILE = "notes_data.pkl"
MODEL_FILE = "music_model.keras"
MAPPING_FILE = "mappings.pkl"
EPOCHS = 40
BATCH_SIZE = 64


def prepare_sequences(notes, sequence_length=SEQUENCE_LENGTH):
    pitch_names = sorted(set(notes))
    note_to_int = {note: i for i, note in enumerate(pitch_names)}
    int_to_note = {i: note for i, note in enumerate(pitch_names)}
    n_vocab = len(pitch_names)

    network_input = []
    network_output = []
    for i in range(len(notes) - sequence_length):
        seq_in = notes[i:i + sequence_length]
        seq_out = notes[i + sequence_length]
        network_input.append([note_to_int[n] for n in seq_in])
        network_output.append(note_to_int[seq_out])

    n_patterns = len(network_input)
    X = np.reshape(network_input, (n_patterns, sequence_length, 1))
    X = X / float(n_vocab)
    y = to_categorical(network_output, num_classes=n_vocab)

    return X, y, note_to_int, int_to_note, n_vocab


def build_model(sequence_length, n_vocab):
    model = Sequential([
        LSTM(128, input_shape=(sequence_length, 1), return_sequences=True),
        Dropout(0.3),
        LSTM(128),
        Dense(128),
        Dropout(0.3),
        Dense(n_vocab),
        Activation("softmax"),
    ])
    model.compile(loss="categorical_crossentropy", optimizer="adam")
    return model


if __name__ == "__main__":
    with open(NOTES_FILE, "rb") as f:
        notes = pickle.load(f)

    X, y, note_to_int, int_to_note, n_vocab = prepare_sequences(notes)
    print(f"Vocabulary size: {n_vocab} unique notes/chords")
    print(f"Training patterns: {X.shape[0]}")

    model = build_model(SEQUENCE_LENGTH, n_vocab)
    model.summary()

    model.fit(X, y, epochs=EPOCHS, batch_size=BATCH_SIZE)

    model.save(MODEL_FILE)
    with open(MAPPING_FILE, "wb") as f:
        pickle.dump(
            {"note_to_int": note_to_int, "int_to_note": int_to_note,
             "n_vocab": n_vocab, "sequence_length": SEQUENCE_LENGTH},
            f,
        )
    print(f"Model saved to {MODEL_FILE}, mappings saved to {MAPPING_FILE}")
