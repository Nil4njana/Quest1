from pathlib import Path

import pytest

from src.frame_extraction import (
    extract_frame,
    get_video_duration,
    get_video_fps,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

VIDEO_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "source.mp4"
)


@pytest.mark.integration
def test_get_video_fps():

    if not VIDEO_PATH.exists():
        pytest.skip(
            f"Video fixture not found: {VIDEO_PATH}"
        )

    fps = get_video_fps(VIDEO_PATH)

    assert fps > 0


@pytest.mark.integration
def test_get_video_duration():

    if not VIDEO_PATH.exists():
        pytest.skip(
            f"Video fixture not found: {VIDEO_PATH}"
        )

    duration = get_video_duration(VIDEO_PATH)

    assert duration > 0


@pytest.mark.integration
def test_extract_frame_creates_image(tmp_path):

    if not VIDEO_PATH.exists():
        pytest.skip(
            f"Video fixture not found: {VIDEO_PATH}"
        )

    output_path = (
        tmp_path / "test_frame.jpg"
    )

    result = extract_frame(
        VIDEO_PATH,
        timestamp=324.740,
        output_path=output_path,
    )

    assert output_path.exists()
    assert result.timestamp == 324.740
    assert result.frame_number > 0


def test_extract_frame_rejects_negative_timestamp(
    tmp_path,
):

    with pytest.raises(ValueError):
        extract_frame(
            VIDEO_PATH,
            timestamp=-1,
            output_path=tmp_path / "frame.jpg",
        )