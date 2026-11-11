from src.domain.soundproof_artist import SoundProofArtist
from typing import Protocol




class ArtistDatabase(Protocol):
    """Lookup of artists in a database of AI-generated music reports."""

    def find(self, artist_name: str) -> SoundProofArtist | None:
        """Return the entry matching the artist name, or None when the artist was never reported."""
        ...
