from pathlib import Path

from src.common.matching import find_first_dialogue
from src.common.transcript import load_word_timestamps


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TRANSCRIPT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "transcripts"
    / "source_words.json"
)


def main() -> None:
    target = input("Enter dialogue: ").strip()

    words = load_word_timestamps(
        TRANSCRIPT_PATH
    )

    result = find_first_dialogue(
        target,
        words,
        threshold=0.80,
    )

    if result is None:
        print("Dialogue not found.")
        return

    print()
    print("FIRST OCCURRENCE")
    print(f"Start:      {result.start:.3f} seconds")
    print(f"End:        {result.end:.3f} seconds")
    print(f"Similarity: {result.similarity:.3f}")
    print(f"Matched:    {result.matched_text}")


if __name__ == "__main__":
    main()