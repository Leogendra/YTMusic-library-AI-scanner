from dataclasses import dataclass




@dataclass(frozen=True)
class RemovalReport:
    """Outcome of the removal of tracks from the library."""

    removed_video_ids: tuple[str, ...]
    not_removed_video_ids: tuple[str, ...]
