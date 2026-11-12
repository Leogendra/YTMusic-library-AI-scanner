from typing import Protocol

class ArtistReleasesUnavailableError(Exception):
    """Raised when the releases of an artist cannot be read, for instance when its channel is not an artist page."""




class ArtistReleaseSource(Protocol):
    """Provider of the release years of an artist."""

    def fetch_release_years(self, channel_id: str) -> list[int]:
        """Return the year of every dated release (albums, EP and singles) of the artist."""
        ...
