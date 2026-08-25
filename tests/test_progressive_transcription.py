from src.approach2.progressive_transcription import merge_words
from src.common.transcription import WordTimestamp


def test_merge_words_orders_by_timestamp():

    existing = [
        WordTimestamp(
            "world",
            2.0,
            2.5,
        )
    ]

    new_words = [
        WordTimestamp(
            "hello",
            1.0,
            1.5,
        )
    ]

    result = merge_words(
        existing,
        new_words,
    )

    assert result == [
        WordTimestamp(
            "hello",
            1.0,
            1.5,
        ),
        WordTimestamp(
            "world",
            2.0,
            2.5,
        ),
    ]
def test_load_progress_returns_empty_for_new_transcript(
    tmp_path,
):

    from src.approach2.progressive_transcription import (
        load_progress,
    )

    transcript_path = (
        tmp_path / "new.json"
    )

    words, timestamp, complete = (
        load_progress(
            transcript_path
        )
    )

    assert words == []
    assert timestamp == 0.0
    assert complete is False