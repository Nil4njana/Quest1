from src.common.matching import (
    find_first_dialogue,
    normalize_text,
)
from src.common.transcription import WordTimestamp


def make_words():
    return [
        WordTimestamp("hello", 1.0, 1.4),
        WordTimestamp("there", 1.4, 1.8),
        WordTimestamp("sorry", 10.0, 10.4),
        WordTimestamp("sir", 10.4, 10.7),
        WordTimestamp("but", 10.7, 10.9),
        WordTimestamp("you", 10.9, 11.1),
        WordTimestamp("cannot", 11.1, 11.5),
        WordTimestamp("come", 11.5, 11.8),
        WordTimestamp("here", 11.8, 12.1),
        WordTimestamp("sorry", 30.0, 30.4),
        WordTimestamp("sir", 30.4, 30.7),
        WordTimestamp("but", 30.7, 30.9),
        WordTimestamp("you", 30.9, 31.1),
        WordTimestamp("cannot", 31.1, 31.5),
        WordTimestamp("come", 31.5, 31.8),
        WordTimestamp("here", 31.8, 32.1),
    ]


def test_normalize_text():
    assert normalize_text(
        "Hello, THERE!"
    ) == ["hello", "there"]


def test_find_first_dialogue():
    words = make_words()

    result = find_first_dialogue(
        "sorry sir but you cannot come here",
        words,
    )

    assert result is not None
    assert result.start == 10.0
    assert result.end == 12.1


def test_first_occurrence_is_returned():
    words = make_words()

    result = find_first_dialogue(
        "sorry sir but you cannot come here",
        words,
    )

    assert result is not None

    # The same dialogue occurs again at 30 seconds.
    # We want the FIRST occurrence.
    assert result.start == 10.0


def test_dialogue_not_found():
    words = make_words()

    result = find_first_dialogue(
        "this dialogue does not exist",
        words,
    )

    assert result is None