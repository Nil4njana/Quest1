from dataclasses import dataclass
import re
from difflib import SequenceMatcher

from src.common.transcription import WordTimestamp


@dataclass(frozen=True)
class MatchResult:
    """Result of a dialogue match."""

    start: float
    end: float
    matched_text: str
    similarity: float


def normalize_text(text: str) -> list[str]:
    """
    Normalize text into comparable tokens.
    """

    text = text.lower()
    text = re.sub(r"[^\w\s']", " ", text)

    return text.split()


def text_similarity(
    target_tokens: list[str],
    candidate_tokens: list[str],
) -> float:
    """
    Calculate sequence similarity between two token lists.
    """

    return SequenceMatcher(
        None,
        target_tokens,
        candidate_tokens,
    ).ratio()


def find_first_dialogue(
    target: str,
    words: list[WordTimestamp],
    threshold: float = 0.80,
) -> MatchResult | None:
    """
    Find the first sufficiently similar occurrence of target dialogue.

    The candidate must begin with the same normalized first word
    as the target, preventing shifted partial matches from being
    accepted too early.
    """

    target_tokens = normalize_text(target)

    if not target_tokens:
        return None

    target_length = len(target_tokens)

    for start_index in range(
        len(words) - target_length + 1
    ):
        window = words[
            start_index : start_index + target_length
        ]

        candidate_tokens = normalize_text(
            " ".join(word.word for word in window)
        )

        if not candidate_tokens:
            continue

        # The timestamp we return corresponds to the first
        # word of the candidate. Therefore require the first
        # word to agree with the target.
        if candidate_tokens[0] != target_tokens[0]:
            continue

        similarity = text_similarity(
            target_tokens,
            candidate_tokens,
        )

        if similarity >= threshold:
            return MatchResult(
                start=window[0].start,
                end=window[-1].end,
                matched_text=" ".join(
                    word.word for word in window
                ),
                similarity=similarity,
            )

    return None