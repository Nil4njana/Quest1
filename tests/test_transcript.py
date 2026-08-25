import json

import pytest

from src.transcription import WordTimestamp
from src.transcript import (
    load_word_timestamps,
    save_word_timestamps,
)


def test_save_word_timestamps(tmp_path):
    words = [
        WordTimestamp("hello", 1.2, 1.6),
        WordTimestamp("world", 1.7, 2.1),
    ]

    output_path = tmp_path / "transcript.json"

    result = save_word_timestamps(
        words,
        output_path,
    )

    assert result == output_path
    assert output_path.exists()

    data = json.loads(
        output_path.read_text(encoding="utf-8")
    )

    assert data == [
        {
            "word": "hello",
            "start": 1.2,
            "end": 1.6,
        },
        {
            "word": "world",
            "start": 1.7,
            "end": 2.1,
        },
    ]


def test_load_word_timestamps(tmp_path):
    output_path = tmp_path / "transcript.json"

    output_path.write_text(
        json.dumps(
            [
                {
                    "word": "hello",
                    "start": 1.2,
                    "end": 1.6,
                },
                {
                    "word": "world",
                    "start": 1.7,
                    "end": 2.1,
                },
            ]
        ),
        encoding="utf-8",
    )

    words = load_word_timestamps(output_path)

    assert words == [
        WordTimestamp("hello", 1.2, 1.6),
        WordTimestamp("world", 1.7, 2.1),
    ]


def test_load_word_timestamps_rejects_missing_file(tmp_path):
    missing_path = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_word_timestamps(missing_path)