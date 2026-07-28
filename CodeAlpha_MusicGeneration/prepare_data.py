"""
CodeAlpha - Task 3: Music Generation with AI
prepare_data.py

Parses a set of MIDI/MusicXML pieces (using music21's bundled Bach chorale
corpus - no external download needed) and converts them into note/chord
sequences suitable for training an LSTM.

Run this once before train.py:
    python prepare_data.py
"""

import pickle
from music21 import corpus, note, chord

NUM_PIECES = 40          # how many bach chorales to train on (keep small for a quick demo)
OUTPUT_NOTES_FILE = "notes_data.pkl"


def get_notes(num_pieces=NUM_PIECES):
    """Extract a flat list of note/chord tokens from bundled Bach chorales."""
    all_notes = []
    bach_paths = corpus.getComposer("bach")[:num_pieces]

    print(f"Parsing {len(bach_paths)} Bach chorales from music21's bundled corpus...")
    for i, path in enumerate(bach_paths):
        try:
            score = corpus.parse(path)
        except Exception as e:
            print(f"  Skipping {path.name}: {e}")
            continue

        parts = score.parts
        notes_to_parse = parts[0].flatten().notes if len(parts) > 0 else score.flatten().notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                all_notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                all_notes.append(".".join(str(n) for n in element.normalOrder))

        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(bach_paths)} pieces...")

    print(f"Total tokens extracted: {len(all_notes)}")
    return all_notes


if __name__ == "__main__":
    notes = get_notes()
    with open(OUTPUT_NOTES_FILE, "wb") as f:
        pickle.dump(notes, f)
    print(f"Saved to {OUTPUT_NOTES_FILE}")
