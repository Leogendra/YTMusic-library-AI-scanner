from src.domain.checked_artist import CheckedArtist
from dataclasses import dataclass




@dataclass(frozen=True)
class ArtistCheckReport:
    """Outcome of the check of the release years of the artists missing from SoundProof."""

    # Ranked from the most suspicious artist to the least suspicious one.
    checked_artists: tuple[CheckedArtist, ...]
    # Artists without artist page, whose page could not be read, or without any dated release.
    unverifiable_artist_count: int
