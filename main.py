from pathlib import Path

from src.common.download import download_video
from src.common.audio import extract_audio

from src.approach1.find_dialogue_frame import (
    find_dialogue_frame,
)

from src.approach2.progressive_find_dialogue_frame import (
    progressive_find_dialogue_frame,
)

from src.common.transcription import AudioTranscriber


PROJECT_ROOT = Path(__file__).resolve().parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
AUDIO_DIR = PROJECT_ROOT / "data" / "audio"
TRANSCRIPT_DIR = PROJECT_ROOT / "outputs" / "transcripts"


def main() -> None:

    print("=" * 60)
    print("AUDIO FRAME IDENTIFIER")
    print("=" * 60)

    video_url = input(
        "\nEnter video URL: "
    ).strip()

    dialogue = input(
        "Enter dialogue: "
    ).strip()

    print(
        "\nChoose approach:"
    )
    print(
        "1. Full transcription"
    )
    print(
        "2. Progressive transcription"
    )

    approach = input(
        "Enter choice (1/2): "
    ).strip()

    if not video_url or not dialogue:
        print("\nNone")
        return

    if approach not in {"1", "2"}:
        print("\nInvalid approach.")
        return

    # ---------------------------------------------------------
    # Download video
    # ---------------------------------------------------------

    video_path = download_video(
        url=video_url,
        output_dir=RAW_DIR,
    )

    # ---------------------------------------------------------
    # Extract audio
    # ---------------------------------------------------------

    audio_path = (
        AUDIO_DIR
        / f"{video_path.stem}.wav"
    )

    extract_audio(
        video_path=video_path,
        output_path=audio_path,
    )

    # ---------------------------------------------------------
    # Select approach
    # ---------------------------------------------------------

    if approach == "1":

        transcript_path = (
            TRANSCRIPT_DIR
            / f"{video_path.stem}_words.json"
        )

        
        result = find_dialogue_frame(
            dialogue=dialogue,
            video_path=video_path,
            audio_path=audio_path,
            transcript_path=transcript_path,
        )  

    else:

        transcript_path = (
            TRANSCRIPT_DIR
            / f"{video_path.stem}_progressive.json"
        )

        transcriber = AudioTranscriber(
            model_size="small.en",
            vad_filter=False,
        )

        result = progressive_find_dialogue_frame(
            dialogue=dialogue,
            video_path=video_path,
            audio_path=audio_path,
            transcript_path=transcript_path,
            transcriber=transcriber,
            threshold=0.80,
            chunk_seconds=30.0,
        )

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    print()

    if result is None:
        print("None")
        return

    print("=" * 60)
    print("RESULT")
    print("=" * 60)

    print(
        f"Timestamp : {result['timestamp_formatted']}"
    )

    print(
        f"Frame     : {result['frame_number']}"
    )

    print(
        f'Text      : "{result["text"]}"'
    )

    print(
        f"Frame saved at: "
        f"{Path(result['frame_path']).resolve()}"
    )


if __name__ == "__main__":
    main()