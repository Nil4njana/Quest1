from dataclasses import dataclass
from pathlib import Path

from faster_whisper import WhisperModel


@dataclass(frozen=True)
class WordTimestamp:
    """A single transcribed word and its time range in seconds."""

    word: str
    start: float
    end: float


def transcribe_audio(
    audio_path: str | Path,
    model_size: str = "small.en",
    vad_filter: bool = False,
) -> list[WordTimestamp]:
    """
    Transcribe an audio file and return word-level timestamps.

    Parameters
    ----------
    audio_path:
        Path to the audio file.

    model_size:
        Faster-Whisper model to use.

    vad_filter:
        Whether to enable voice activity detection.

    Returns
    -------
    list[WordTimestamp]
        Transcribed words with start and end timestamps.
    """

    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    model = WhisperModel(
        model_size,
        device="cpu",
        compute_type="int8",
    )

    segments, _ = model.transcribe(
        str(audio_path),
        language="en",
        word_timestamps=True,
        vad_filter=vad_filter,
        beam_size=5,
        condition_on_previous_text=False,
    )

    words: list[WordTimestamp] = []

    for segment in segments:
        if segment.words is None:
            continue

        for word in segment.words:
            cleaned_word = word.word.strip()

            if not cleaned_word:
                continue

            words.append(
                WordTimestamp(
                    word=cleaned_word,
                    start=float(word.start),
                    end=float(word.end),
                )
            )

    return words