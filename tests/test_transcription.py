from pathlib import Path

import pytest

from src.common.transcription import (
    AudioTranscriber,
    WordTimestamp,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

AUDIO_PATH = (
    PROJECT_ROOT
    / "data"
    / "audio"
    / "test_clip_10min.wav"
)


@pytest.fixture(scope="module")
def transcriber():
    """
    Create one transcriber for this test module.

    The Whisper model is loaded once and reused
    by all tests in this module.
    """

    return AudioTranscriber(
        model_size="small.en",
        vad_filter=False,
    )


@pytest.fixture
def words(transcriber):
    """Transcribe the test audio once for each test."""

    if not AUDIO_PATH.exists():
        pytest.skip(
            f"Test audio fixture not found: {AUDIO_PATH}"
        )

    return transcriber.transcribe(AUDIO_PATH)


@pytest.mark.integration
def test_transcription_returns_word_timestamps(words):
    assert words

    assert all(
        isinstance(word, WordTimestamp)
        for word in words
    )

    for word in words:
        assert word.word
        assert word.start >= 0
        assert word.end >= word.start


@pytest.mark.integration
def test_transcription_words_are_time_ordered(words):
    assert words

    for previous, current in zip(words, words[1:]):
        assert current.start >= previous.start