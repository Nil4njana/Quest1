from dataclasses import asdict
from pathlib import Path
import json

from src.common.probe import get_media_duration
from src.common.transcription import (
    AudioTranscriber,
    WordTimestamp,
)


def merge_words(
    existing: list[WordTimestamp],
    new_words: list[WordTimestamp],
) -> list[WordTimestamp]:
    """
    Merge newly transcribed words with previously
    transcribed words.

    Words are ordered chronologically.
    """

    combined = existing + new_words

    combined.sort(
        key=lambda word: (
            word.start,
            word.end,
        )
    )

    return combined


def save_progress(
    words: list[WordTimestamp],
    transcript_path: str | Path,
    *,
    audio_path: str | Path,
    transcribed_until: float,
    complete: bool,
) -> None:
    """
    Save progressive transcription state.

    This state belongs specifically to
    Approach 2.
    """

    transcript_path = Path(
        transcript_path
    )

    transcript_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = {
        "audio_path": str(
            Path(audio_path).resolve()
        ),
        "transcribed_until": (
            transcribed_until
        ),
        "complete": complete,
        "words": [
            asdict(word)
            for word in words
        ],
    }

    transcript_path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def load_progress(
    transcript_path: str | Path,
) -> tuple[
    list[WordTimestamp],
    float,
    bool,
]:
    """
    Load previously saved progressive
    transcription state.

    Returns:

        words
        transcribed_until
        complete
    """

    transcript_path = Path(
        transcript_path
    )

    if not transcript_path.exists():
        return [], 0.0, False

    data = json.loads(
        transcript_path.read_text(
            encoding="utf-8"
        )
    )

    words = [
        WordTimestamp(
            item["word"],
            item["start"],
            item["end"],
        )
        for item in data.get(
            "words",
            [],
        )
    ]

    return (
        words,
        float(
            data.get(
                "transcribed_until",
                0.0,
            )
        ),
        bool(
            data.get(
                "complete",
                False,
            )
        ),
    )


def transcribe_next_chunk(
    transcriber: AudioTranscriber,
    audio_path: str | Path,
    *,
    start_time: float,
    chunk_seconds: float,
    duration: float | None = None,
) -> tuple[
    list[WordTimestamp],
    float,
]:
    """
    Transcribe one chunk of audio.

    If duration is not supplied, obtain it
    using the common FFprobe duration utility.

    Returns:

        newly transcribed words
        end timestamp of the chunk
    """

    audio_path = Path(
        audio_path
    )

    if duration is None:
        duration = get_media_duration(
            audio_path
        )

    if start_time >= duration:
        return [], duration

    end_time = min(
        start_time + chunk_seconds,
        duration,
    )

    words = transcriber.transcribe_segment(
        audio_path,
        start_time=start_time,
        end_time=end_time,
    )

    return words, end_time