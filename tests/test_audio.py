from pathlib import Path

from src.audio import extract_audio


PROJECT_ROOT = Path(__file__).resolve().parents[1]

VIDEO_PATH = PROJECT_ROOT / "data" / "raw" / "source.mp4"
AUDIO_PATH = PROJECT_ROOT / "data" / "audio" / "source.wav"


def test_extract_audio_creates_wav():
    output = extract_audio(
        video_path=VIDEO_PATH,
        output_path=AUDIO_PATH,
    )

    assert output.exists()
    assert output.suffix == ".wav"


def test_extract_audio_rejects_missing_video(tmp_path):
    missing_video = tmp_path / "missing.mp4"
    output_audio = tmp_path / "audio.wav"

    try:
        extract_audio(
            video_path=missing_video,
            output_path=output_audio,
        )
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass