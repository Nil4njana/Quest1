from dataclasses import dataclass
from pathlib import Path

from faster_whisper import WhisperModel


@dataclass(frozen=True)
class WordTimestamp:
    """A single transcribed word and its time range in seconds."""

    word: str
    start: float
    end: float


class AudioTranscriber:
    """
    Reusable speech-to-text transcriber.

    The Whisper model is loaded once when the object is created
    and reused for every transcription performed by this object.
    """

    def __init__(
        self,
        model_size: str = "small.en",
        vad_filter: bool = False,
    ) -> None:
        self.model_size = model_size
        self.vad_filter = vad_filter

        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
        )

    def transcribe(
        self,
        audio_path: str | Path,
    ) -> list[WordTimestamp]:
        """
        Transcribe an entire audio file and return
        word-level timestamps.
        """

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        segments, _ = self.model.transcribe(
            str(audio_path),
            language="en",
            word_timestamps=True,
            vad_filter=self.vad_filter,
            beam_size=5,
            condition_on_previous_text=False,
        )

        return self._extract_words(
            segments,
            offset=0.0,
        )

    def transcribe_segment(
        self,
        audio_path: str | Path,
        *,
        start_time: float,
        end_time: float,
    ) -> list[WordTimestamp]:
        """
        Transcribe only a portion of an audio file.

        The returned timestamps are absolute timestamps
        relative to the original audio file.
        """

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        if start_time < 0:
            raise ValueError(
                "start_time must be >= 0"
            )

        if end_time <= start_time:
            raise ValueError(
                "end_time must be greater than start_time"
            )

        segments, _ = self.model.transcribe(
            str(audio_path),
            language="en",
            word_timestamps=True,
            vad_filter=self.vad_filter,
            beam_size=5,
            condition_on_previous_text=False,
            clip_timestamps=(
                start_time,
                end_time,
            ),
        )

        return self._extract_words(
            segments,
            offset=0.0,
        )

    @staticmethod
    def _extract_words(
        segments,
        *,
        offset: float = 0.0,
    ) -> list[WordTimestamp]:
        """
        Convert Faster-Whisper segments into
        WordTimestamp objects.
        """

        words: list[WordTimestamp] = []

        for segment in segments:

            if segment.words is None:
                continue

            for word in segment.words:

                cleaned_word = (
                    word.word.strip()
                )

                if not cleaned_word:
                    continue

                words.append(
                    WordTimestamp(
                        word=cleaned_word,
                        start=(
                            float(word.start)
                            + offset
                        ),
                        end=(
                            float(word.end)
                            + offset
                        ),
                    )
                )

        return words