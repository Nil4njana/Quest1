from pathlib import Path
import re

from src.common.frame_extraction import extract_frame
from src.common.matching import find_first_dialogue
from src.common.transcript import (
    load_word_timestamps,
    save_word_timestamps,
)
from src.common.transcription import AudioTranscriber


def sanitize_filename(text: str) -> str:
    """
    Convert dialogue text into a safe filename.
    """

    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s-]",
        "",
        text,
    )

    text = re.sub(
        r"\s+",
        "_",
        text,
    )

    return text


def format_timestamp(seconds: float) -> str:
    """
    Convert seconds to HH:MM:SS.sss.
    """

    hours = int(
        seconds // 3600
    )

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


def find_dialogue_frame(
    dialogue: str,
    video_path: str | Path,
    audio_path: str | Path,
    transcript_path: str | Path,
    *,
    threshold: float = 0.80,
) -> dict | None:
    """
    Approach 1:

    Use a complete saved transcript when available.

    If the transcript does not exist, transcribe the
    complete audio first and save it for future searches.

    Then find the first occurrence of the dialogue and
    extract the corresponding frame.
    """

    video_path = Path(
        video_path
    )

    audio_path = Path(
        audio_path
    )

    transcript_path = Path(
        transcript_path
    )

    frame_output_dir = (
        Path("outputs")
        / "frames"
    )

    frame_output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ---------------------------------------------------------
    # 1. Load existing transcript or create it
    # ---------------------------------------------------------

    if transcript_path.exists():

        print(
            "Existing transcript found."
        )

        print(
            f"Loading: "
            f"{transcript_path.resolve()}"
        )

        words = load_word_timestamps(
            transcript_path
        )

    else:

        print(
            "No existing transcript found."
        )

        print(
            "Starting full-video transcription..."
        )

        transcriber = AudioTranscriber(
            model_size="small.en",
            vad_filter=False,
        )

        words = transcriber.transcribe(
            audio_path
        )

        save_word_timestamps(
            words,
            transcript_path,
        )

        print(
            f"Transcript saved: "
            f"{transcript_path.resolve()}"
        )

    # ---------------------------------------------------------
    # 2. Find first dialogue occurrence
    # ---------------------------------------------------------

    result = find_first_dialogue(
        dialogue,
        words,
        threshold=threshold,
    )

    if result is None:
        return None

    # ---------------------------------------------------------
    # 3. Extract corresponding frame
    # ---------------------------------------------------------

    safe_dialogue = sanitize_filename(
        dialogue
    )

    video_name = video_path.stem

    frame_path = (
        frame_output_dir
        / f"{video_name}_{safe_dialogue}.jpg"
    )

    frame = extract_frame(
        video_path,
        timestamp=result.start,
        output_path=frame_path,
    )

    # ---------------------------------------------------------
    # 4. Return result
    # ---------------------------------------------------------

    return {
        "timestamp": frame.timestamp,
        "timestamp_formatted": (
            format_timestamp(
                frame.timestamp
            )
        ),
        "frame_number": frame.frame_number,
        "text": dialogue,
        "similarity": result.similarity,
        "frame_path": frame.output_path,
    }