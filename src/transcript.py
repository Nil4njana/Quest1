import json
from pathlib import Path

from src.transcription import WordTimestamp


def save_word_timestamps(
    words: list[WordTimestamp],
    output_path: str | Path,
) -> Path:
    """Save word-level timestamps to a JSON file."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = [
        {
            "word": word.word,
            "start": word.start,
            "end": word.end,
        }
        for word in words
    ]

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return output_path


def load_word_timestamps(
    input_path: str | Path,
) -> list[WordTimestamp]:
    """Load word-level timestamps from a JSON file."""

    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Transcript file not found: {input_path}"
        )

    with input_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        WordTimestamp(
            word=item["word"],
            start=float(item["start"]),
            end=float(item["end"]),
        )
        for item in data
    ]