def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS.sss."""

    hours = int(seconds // 3600)

    minutes = int(
        (seconds % 3600) // 60
    )

    remaining_seconds = (
        seconds % 60
    )

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{remaining_seconds:06.3f}"
    )