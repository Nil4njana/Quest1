from pathlib import Path
import subprocess


def extract_audio(
    video_path: str | Path,
    output_path: str | Path,
    sample_rate: int = 16000,
    channels: int = 1,
) -> Path:
    """
    Extract the audio track from a video using FFmpeg.

    The output is an uncompressed WAV file, which is convenient
    for downstream speech-recognition processing.
    """

    video_path = Path(video_path)
    output_path = Path(output_path)

    if not video_path.exists():
        raise FileNotFoundError(
            f"Video file not found: {video_path}"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),

        # Audio only
        "-vn",

        # WAV / PCM format
        "-acodec",
        "pcm_s16le",

        # Speech-friendly audio settings
        "-ar",
        str(sample_rate),
        "-ac",
        str(channels),

        str(output_path),
    ]

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            "FFmpeg failed while extracting audio.\n"
            f"{error.stderr}"
        ) from error

    if not output_path.exists():
        raise RuntimeError(
            f"FFmpeg completed but output was not created: "
            f"{output_path}"
        )

    return output_path