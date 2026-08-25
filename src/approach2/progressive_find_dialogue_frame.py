from pathlib import Path
import re
from src.common.frame_extraction import extract_frame
from src.approach2.progressive_search import progressive_search
from src.common.transcription import AudioTranscriber
from src.common.time_utils import format_timestamp

OUTPUT_DIR = Path("outputs/frames")


def sanitize_filename(text: str) -> str:
    """
    Convert dialogue text into a safe filename.
    """

    text = text.lower().strip()

    text = re.sub(
        r"[^\w\s-]",
        "",
        text,
    )

    text = re.sub(
        r"\s+",
        "_",
        text,
    )

    return text




def progressive_find_dialogue_frame(
    dialogue: str,
    video_path: str | Path,
    audio_path: str | Path,
    transcript_path: str | Path,
    *,
    transcriber: AudioTranscriber,
    threshold: float = 0.80,
    chunk_seconds: float = 30.0,
) -> dict | None:

    video_path = Path(video_path)

    audio_path = Path(audio_path)

    transcript_path = Path(
        transcript_path
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    result = progressive_search(
        dialogue,
        audio_path,
        transcript_path,
        transcriber=transcriber,
        chunk_seconds=chunk_seconds,
        threshold=threshold,
    )

    if not result.found:
        return None

    timestamp = result.start

    # Get FPS so we can report the frame number.
   

    safe_dialogue = sanitize_filename(
        dialogue
    )

    video_id = video_path.stem

    frame_path = (
        OUTPUT_DIR
        / f"{video_id}_{safe_dialogue}.jpg"
    )

    # Extract the frame corresponding
    # to the dialogue start timestamp.
    frame = extract_frame(
    video_path,
    timestamp,
    frame_path,
    )

    print()
    print(
        f"Timestamp: "
        f"{format_timestamp(timestamp)}"
    )

    print(
        f"Frame:     {frame.frame_number}"
    )

    print(
        f'Text:      "{result.matched_text}"'
    )

    print(
        f"Frame saved: "
        f"{frame_path.resolve()}"
    )

    return {
        "timestamp": timestamp,
        "timestamp_formatted": (
            format_timestamp(timestamp)
        ),
        "frame_number": frame.frame_number,
        "text": result.matched_text,
        "similarity": result.similarity,
        "frame_path": frame_path,
    }


if __name__ == "__main__":

    VIDEO_PATH = Path(
        "data/raw/aS4sjwPws8I.mp4"
    )

    AUDIO_PATH = Path(
        "data/audio/aS4sjwPws8I.wav"
    )

    TRANSCRIPT_PATH = Path(
        "outputs/transcripts/"
        "aS4sjwPws8I_progressive.json"
    )

    dialogue = (
        "please clap"
    )

    transcriber = AudioTranscriber(
        model_size="small.en",
        vad_filter=False,
    )

    result = progressive_find_dialogue_frame(
        dialogue,
        VIDEO_PATH,
        AUDIO_PATH,
        TRANSCRIPT_PATH,
        transcriber=transcriber,
        threshold=0.80,
        chunk_seconds=30.0,
    )

    print()

    if result is None:

        print("None")

    else:

        print(
            "Progressive search completed."
        )