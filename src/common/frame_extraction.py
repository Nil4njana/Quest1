import json
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FrameResult:
    timestamp: float
    frame_number: int
    output_path: Path


def get_video_fps(video_path: str | Path) -> float:
    """Return the average video frame rate."""

    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(
            f"Video file not found: {video_path}"
        )

    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=avg_frame_rate",
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

    data = json.loads(completed.stdout)

    fps_string = data["streams"][0]["avg_frame_rate"]

    numerator, denominator = map(
        int,
        fps_string.split("/"),
    )

    return numerator / denominator


def get_video_duration(video_path: str | Path) -> float:
    """Return video duration in seconds."""

    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(
            f"Video file not found: {video_path}"
        )

    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]

    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

    return float(completed.stdout.strip())


def extract_frame(
    video_path: str | Path,
    timestamp: float,
    output_path: str | Path,
) -> FrameResult:
    """
    Extract one frame from a video at the given timestamp.

    Returns the timestamp, frame number and generated image path.
    """

    video_path = Path(video_path)
    output_path = Path(output_path)

    if timestamp < 0:
        raise ValueError("Timestamp cannot be negative.")

    duration = get_video_duration(video_path)

    if timestamp > duration:
        raise ValueError(
            f"Timestamp {timestamp:.3f}s is outside "
            f"the video duration ({duration:.3f}s)."
        )

    fps = get_video_fps(video_path)

    frame_number = round(timestamp * fps)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    command = [
        "ffmpeg",
        "-y",
        "-ss",
        f"{timestamp:.3f}",
        "-i",
        str(video_path),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output_path),
    ]

    subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

    if not output_path.exists():
        raise RuntimeError(
            f"FFmpeg did not create frame: {output_path}"
        )

    return FrameResult(
        timestamp=timestamp,
        frame_number=frame_number,
        output_path=output_path,
    )