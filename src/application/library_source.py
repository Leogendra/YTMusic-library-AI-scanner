from src.domain.library_track import LibraryTrack
from typing import Protocol




class LibrarySource(Protocol):
    """Provider of the tracks saved in a user's music library."""

    def fetch_tracks(self) -> list[LibraryTrack]:
        """Return every track of the library."""
        ...
