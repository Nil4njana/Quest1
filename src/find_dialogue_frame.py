from pathlib import Path

from src.frame_extraction import extract_frame
from src.matching import find_first_dialogue
from src.transcript import load_word_timestamps


PROJECT_ROOT = Path(__file__).resolve().parents[1]

VIDEO_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "source.mp4"
)

TRANSCRIPT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "transcripts"
    / "source_words.json"
)

FRAME_OUTPUT_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "frames"
)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS.sss."""

    hours = int(seconds // 3600)

    minutes = int(
        (seconds % 3600) // 60
    )

    remaining_seconds = (
        seconds % 60
    )

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{remaining_seconds:06.3f}"
    )


def main() -> None:

    target = input(
        "Enter dialogue: "
    ).strip()

    if not target:
        print("None")
        return

    words = load_word_timestamps(
        TRANSCRIPT_PATH
    )

    result = find_first_dialogue(
        target,
        words,
        threshold=0.80,
    )

    if result is None:
        print("None")
        return

    frame_path = (
        FRAME_OUTPUT_DIR
        / "first_occurrence.jpg"
    )

    frame = extract_frame(
        VIDEO_PATH,
        timestamp=result.start,
        output_path=frame_path,
    )

    print()
    print(
        f"Timestamp : "
        f"{format_timestamp(frame.timestamp)}"
    )

    print(
        f"Frame     : "
        f"{frame.frame_number}"
    )

    print(
        f'Text      : "{target}"'
    )

    print(
        f"Frame saved: {frame.output_path}"
    )


if __name__ == "__main__":
    main()