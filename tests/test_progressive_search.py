from unittest.mock import patch

from src.approach2.progressive_search import (
    progressive_search,
)
from src.common.transcription import WordTimestamp


class FakeTranscriber:
    """
    Fake transcriber used to test progressive-search
    logic without loading Whisper.
    """

    def __init__(self):
        self.calls = []

    def transcribe_segment(
        self,
        audio_path,
        *,
        start_time,
        end_time,
    ):
        self.calls.append(
            (
                start_time,
                end_time,
            )
        )

        if start_time == 0.0:
            return [
                WordTimestamp(
                    "hello",
                    0.0,
                    0.5,
                )
            ]

        if start_time == 30.0:
            return [
                WordTimestamp(
                    "sorry",
                    30.0,
                    30.4,
                ),
                WordTimestamp(
                    "sir",
                    30.4,
                    30.7,
                ),
                WordTimestamp(
                    "but",
                    30.7,
                    30.9,
                ),
                WordTimestamp(
                    "you",
                    30.9,
                    31.1,
                ),
            ]

        return []


def test_progressive_search_stops_when_dialogue_found(
    tmp_path,
):
    audio_path = (
        tmp_path / "audio.wav"
    )

    audio_path.write_bytes(
        b"fake audio"
    )

    transcript_path = (
        tmp_path / "transcript.json"
    )

    transcriber = FakeTranscriber()

    with patch(
        "src.approach2.progressive_search.get_media_duration",
        return_value=60.0,
    ):

        result = progressive_search(
            "sorry sir but you",
            audio_path,
            transcript_path,
            transcriber=transcriber,
            chunk_seconds=30.0,
            threshold=0.80,
        )

    assert result.found

    assert result.start == 30.0

    assert result.matched_text == (
        "sorry sir but you"
    )

    assert result.similarity >= 0.80

    # Critical hard-stop check:
    #
    # The system should transcribe only:
    #
    #   0 → 30
    #   30 → 60
    #
    # and stop immediately after finding
    # the dialogue.
    assert transcriber.calls == [
        (0.0, 30.0),
        (30.0, 60.0),
    ]

    assert transcript_path.exists()


def test_progressive_search_uses_saved_transcript(
    tmp_path,
):
    audio_path = (
        tmp_path / "audio.wav"
    )

    audio_path.write_bytes(
        b"fake audio"
    )

    transcript_path = (
        tmp_path / "transcript.json"
    )

    # Create a previously saved checkpoint.
    from src.approach2.progressive_transcription import (
        save_progress,
    )

    saved_words = [
        WordTimestamp(
            "sorry",
            10.0,
            10.4,
        ),
        WordTimestamp(
            "sir",
            10.4,
            10.7,
        ),
        WordTimestamp(
            "but",
            10.7,
            10.9,
        ),
        WordTimestamp(
            "you",
            10.9,
            11.1,
        ),
    ]

    save_progress(
        saved_words,
        transcript_path,
        audio_path=audio_path,
        transcribed_until=30.0,
        complete=False,
    )

    transcriber = FakeTranscriber()

    with patch(
        "src.approach2.progressive_search.get_media_duration",
        return_value=60.0,
    ):

        result = progressive_search(
            "sorry sir but you",
            audio_path,
            transcript_path,
            transcriber=transcriber,
            chunk_seconds=30.0,
            threshold=0.80,
        )

    assert result.found

    assert result.start == 10.0

    # Because the dialogue was already in the
    # saved transcript, Whisper must not be called.
    assert transcriber.calls == []