from dataclasses import dataclass
from pathlib import Path

from src.common.matching import (
    MatchResult,
    find_first_dialogue,
)
from src.common.probe import get_media_duration
from src.approach2.progressive_transcription import (
    load_progress,
    merge_words,
    save_progress,
    transcribe_next_chunk,
)
from src.common.transcription import (
    AudioTranscriber,
    WordTimestamp,
)


@dataclass(frozen=True)
class ProgressiveSearchResult:
    """
    Result returned by Approach 2.
    """

    found: bool
    start: float | None
    end: float | None
    matched_text: str | None
    similarity: float
    words: list[WordTimestamp]
    transcribed_until: float


def progressive_search(
    dialogue: str,
    audio_path: str | Path,
    transcript_path: str | Path,
    *,
    transcriber: AudioTranscriber,
    chunk_seconds: float = 30.0,
    threshold: float = 0.80,
) -> ProgressiveSearchResult:
    """
    Progressively transcribe audio until the
    dialogue is encountered.

    Existing transcript progress is reused.

    Transcription stops immediately when a
    match is found.
    """

    audio_path = Path(
        audio_path
    )

    transcript_path = Path(
        transcript_path
    )

    # ---------------------------------------------------------
    # 1. Load existing transcription progress
    # ---------------------------------------------------------

    (
        words,
        transcribed_until,
        complete,
    ) = load_progress(
        transcript_path
    )

    # ---------------------------------------------------------
    # 2. Search the already saved transcript FIRST
    # ---------------------------------------------------------

    existing_match = find_first_dialogue(
        dialogue,
        words,
        threshold=threshold,
    )

    if existing_match is not None:

        return ProgressiveSearchResult(
            found=True,
            start=existing_match.start,
            end=existing_match.end,
            matched_text=(
                existing_match.matched_text
            ),
            similarity=(
                existing_match.similarity
            ),
            words=words,
            transcribed_until=(
                transcribed_until
            ),
        )

    # ---------------------------------------------------------
    # 3. If entire audio was already transcribed,
    #    there is nothing more to transcribe.
    # ---------------------------------------------------------

    if complete:

        return ProgressiveSearchResult(
            found=False,
            start=None,
            end=None,
            matched_text=None,
            similarity=0.0,
            words=words,
            transcribed_until=(
                transcribed_until
            ),
        )

    # ---------------------------------------------------------
    # 4. Get duration ONCE
    # ---------------------------------------------------------

    duration = get_media_duration(
        audio_path
    )

    # ---------------------------------------------------------
    # 5. Continue from saved checkpoint
    # ---------------------------------------------------------

    while True:

        chunk_end_target = min(
            transcribed_until + chunk_seconds,
            duration,
        )

        print(
            f"Transcribing "
            f"{transcribed_until:.2f}s → "
            f"{chunk_end_target:.2f}s"
        )

        new_words, chunk_end = (
            transcribe_next_chunk(
                transcriber,
                audio_path,
                start_time=(
                    transcribed_until
                ),
                chunk_seconds=(
                    chunk_seconds
                ),
                duration=duration,
            )
        )

        # -----------------------------------------------------
        # 6. Merge newly transcribed words
        # -----------------------------------------------------

        words = merge_words(
            words,
            new_words,
        )

        transcribed_until = (
            chunk_end
        )

        # -----------------------------------------------------
        # 7. Determine whether the whole audio is now
        #    transcribed
        # -----------------------------------------------------

        complete = (
            transcribed_until
            >= duration
        )

        # -----------------------------------------------------
        # 8. Save progress immediately
        # -----------------------------------------------------

        save_progress(
            words,
            transcript_path,
            audio_path=audio_path,
            transcribed_until=(
                transcribed_until
            ),
            complete=complete,
        )

        # -----------------------------------------------------
        # 9. Search the accumulated transcript
        # -----------------------------------------------------

        match = find_first_dialogue(
            dialogue,
            words,
            threshold=threshold,
        )

        if match is not None:

            print(
                "Dialogue encountered."
            )

            print(
                "Stopping transcription."
            )

            return ProgressiveSearchResult(
                found=True,
                start=match.start,
                end=match.end,
                matched_text=(
                    match.matched_text
                ),
                similarity=(
                    match.similarity
                ),
                words=words,
                transcribed_until=(
                    transcribed_until
                ),
            )

        # -----------------------------------------------------
        # 10. End of audio
        # -----------------------------------------------------

        if complete:

            return ProgressiveSearchResult(
                found=False,
                start=None,
                end=None,
                matched_text=None,
                similarity=0.0,
                words=words,
                transcribed_until=(
                    transcribed_until
                ),
            )