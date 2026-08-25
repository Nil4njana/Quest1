import json
import subprocess
from pathlib import Path


def probe_video(video_path: str | Path) -> dict:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_streams",
        "-show_format",
        "-of",
        "json",
        str(video_path),
    ]

    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

    return json.loads(completed.stdout)

def get_media_duration(
    media_path: str | Path,
) -> float:
    """
    Return media duration in seconds.
    """

    info = probe_video(media_path)

    return float(
        info["format"]["duration"]
    )