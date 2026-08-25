from pathlib import Path
import subprocess
import sys


VIDEO_URL = "https://ok.ru/video/248244667877"
OUTPUT_DIR = Path("data/raw")


def download_video(url: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    output_template = output_dir / "source.%(ext)s"

    command = [
        sys.executable,
        "-m",
        "yt_dlp",

        # URL
        url,

        # Output
        "-o",
        str(output_template),

        # Download a single video, not a playlist
        "--no-playlist",

        # Prefer MP4
        "-f",
        "best[ext=mp4]/best",

        # Merge into MP4 when necessary
        "--merge-output-format",
        "mp4",

        # Network reliability
        "--socket-timeout",
        "120",
        "--retries",
        "30",
        "--fragment-retries",
        "30",
        "--extractor-retries",
        "10",

        # Do not silently skip missing HLS fragments
        "--no-skip-unavailable-fragments",

        # Download a few fragments concurrently
        "--concurrent-fragments",
        "4",

        # Wait before retrying
        "--retry-sleep",
        "fragment:exp=3:20",

        # Continue/resume partial downloads
        "--continue",

        # Show useful progress
        "--progress",
    ]

    print("Starting video download...")
    print(f"URL: {url}")
    print(f"Output: {output_dir.resolve()}")
    print()

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as error:
        print()
        print("ERROR: Video download failed.")
        print(f"yt-dlp exit code: {error.returncode}")
        raise

    candidates = sorted(output_dir.glob("source.*"))

    if not candidates:
        raise FileNotFoundError(
            f"No downloaded video found in {output_dir.resolve()}"
        )

    video_path = candidates[0]

    print()
    print("Download completed.")
    print(f"Video: {video_path.resolve()}")

    return video_path


if __name__ == "__main__":
    download_video(
        url=VIDEO_URL,
        output_dir=OUTPUT_DIR,
    )