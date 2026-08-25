from pathlib import Path

import pytest

from src.transcription import WordTimestamp, transcribe_audio


PROJECT_ROOT = Path(__file__).resolve().parents[1]

AUDIO_PATH = (
    PROJECT_ROOT
    / "data"
    / "audio"
    / "test_clip_10min.wav"
)


@pytest.mark.integration
def test_transcription_returns_word_timestamps():
    """Verify that the ASR model produces timestamped words."""

    if not AUDIO_PATH.exists():
        pytest.skip(
            f"Test audio fixture not found: {AUDIO_PATH}"
        )

    words = transcribe_audio(AUDIO_PATH)

    assert words
    assert all(isinstance(word, WordTimestamp) for word in words)

    for word in words:
        assert word.word
        assert word.start >= 0
        assert word.end >= word.start


@pytest.mark.integration
def test_transcription_words_are_time_ordered():
    """Verify that word timestamps occur in chronological order."""

    if not AUDIO_PATH.exists():
        pytest.skip(
            f"Test audio fixture not found: {AUDIO_PATH}"
        )

    words = transcribe_audio(AUDIO_PATH)

    assert words

    for previous, current in zip(words, words[1:]):
        assert current.start >= previous.start