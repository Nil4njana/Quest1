from pathlib import Path
import hashlib
import json
import subprocess
import sys
from urllib.parse import urlsplit, urlunsplit


REGISTRY_FILE = "video_registry.json"


def download_video(
    url: str,
    output_dir: str | Path,
) -> Path:
    """
    Download a video only once.

    If the same URL has already been downloaded,
    reuse the existing file instead of downloading
    it again.

    Videos are stored as:

        video_001.mp4
        video_002.webm
        video_003.mkv
        ...
    """

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    registry_path = (
        output_dir / REGISTRY_FILE
    )

    registry = _load_registry(
        registry_path
    )

    normalized_url = _normalize_url(
        url
    )

    video_key = _video_key(
        normalized_url
    )

    # ---------------------------------------------------------
    # 1. Reuse existing download
    # ---------------------------------------------------------

    if video_key in registry:

        existing_video = (
            output_dir
            / registry[video_key]["path"]
        )

        if existing_video.exists():

            print(
                "Existing video found."
            )

            print(
                f"Reusing: {existing_video.resolve()}"
            )

            return existing_video

        # Registry entry exists but file was deleted.
        del registry[video_key]

    # ---------------------------------------------------------
    # 2. Allocate next filename
    # ---------------------------------------------------------

    video_number = 1

    while True:

        prefix = (
            f"video_{video_number:03d}"
        )

        if not list(
            output_dir.glob(
                f"{prefix}.*"
            )
        ):
            break

        video_number += 1

    output_template = (
        output_dir
        / f"{prefix}.%(ext)s"
    )

    # ---------------------------------------------------------
    # 3. Download
    # ---------------------------------------------------------

    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        url,
        "-o",
        str(output_template),
        "--no-playlist",
        "-f",
        (
            "bestvideo+bestaudio"
            "/best"
        ),
        "--merge-output-format",
        "mp4",
        "--socket-timeout",
        "120",
        "--retries",
        "30",
        "--fragment-retries",
        "30",
        "--extractor-retries",
        "10",
        "--no-skip-unavailable-fragments",
        "--concurrent-fragments",
        "4",
        "--retry-sleep",
        "fragment:exp=3:20",
        "--continue",
        "--progress",
    ]

    print(
        "Starting video download..."
    )

    print(f"URL: {url}")

    print(
        f"Output: {output_dir.resolve()}"
    )

    print()

    try:

        subprocess.run(
            command,
            check=True,
        )

    except subprocess.CalledProcessError as error:

        print()

        print(
            "ERROR: Video download failed."
        )

        print(
            f"yt-dlp exit code: {error.returncode}"
        )

        raise

    # ---------------------------------------------------------
    # 4. Locate downloaded file
    # ---------------------------------------------------------

    downloaded_files = [
        path
        for path in sorted(
            output_dir.glob(
                f"{prefix}.*"
            )
        )
        if path.suffix.lower()
        not in {
            ".part",
            ".temp",
            ".ytdl",
        }
    ]

    if not downloaded_files:

        raise FileNotFoundError(
            "Download completed, but the video "
            "could not be located."
        )

    video_path = downloaded_files[0]

    # ---------------------------------------------------------
    # 5. Register for future reuse
    # ---------------------------------------------------------

    registry[video_key] = {
        "url": normalized_url,
        "path": video_path.name,
    }

    _save_registry(
        registry,
        registry_path,
    )

    print()

    print(
        "Download completed."
    )

    print(
        f"Video: {video_path.resolve()}"
    )

    return video_path


# =============================================================
# Registry helpers
# =============================================================


def _normalize_url(
    url: str,
) -> str:
    """
    Normalize a URL so the same video URL maps to
    the same registry entry.

    Fragments (#...) are removed.
    """

    parts = urlsplit(url)

    return urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            parts.path,
            parts.query,
            "",
        )
    )


def _video_key(
    url: str,
) -> str:
    """
    Stable identifier for a video URL.
    """

    return hashlib.sha256(
        url.encode("utf-8")
    ).hexdigest()


def _load_registry(
    registry_path: Path,
) -> dict:

    if not registry_path.exists():
        return {}

    return json.loads(
        registry_path.read_text(
            encoding="utf-8"
        )
    )


def _save_registry(
    registry: dict,
    registry_path: Path,
) -> None:

    registry_path.write_text(
        json.dumps(
            registry,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":

    url = input(
        "Enter video URL: "
    ).strip()

    if not url:
        raise SystemExit(
            "No URL provided."
        )

    download_video(
        url=url,
        output_dir="data/raw",
    )