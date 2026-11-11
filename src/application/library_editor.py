from src.domain.removal_report import RemovalReport
from typing import Protocol




class LibraryEditor(Protocol):
    """Editor of the tracks saved in a user's music library."""

    def remove_tracks(self, video_ids: list[str]) -> RemovalReport:
        """Remove the tracks from the library and tell which ones could not be removed."""
        ...
