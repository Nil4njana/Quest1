from pathlib import Path

from src.common.transcript import save_word_timestamps
from src.common.transcription import AudioTranscriber


PROJECT_ROOT = Path(__file__).resolve().parents[1]

AUDIO_PATH = (
    PROJECT_ROOT
    / "data"
    / "audio"
    / "source.wav"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "transcripts"
    / "source_words.json"
)


def main() -> None:
    print("Starting full-video transcription...")
    print(f"Audio: {AUDIO_PATH}")

    # Load the Whisper model exactly once.
    transcriber = AudioTranscriber(
        model_size="small.en",
        vad_filter=False,
    )

    print("Whisper model loaded.")
    print("Transcribing entire audio...")

    words = transcriber.transcribe(AUDIO_PATH)

    print(f"Words detected: {len(words)}")

    output_path = save_word_timestamps(
        words,
        OUTPUT_PATH,
    )

    print(f"Transcript saved to: {output_path}")


if __name__ == "__main__":
    main()