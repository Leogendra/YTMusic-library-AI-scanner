from src.domain.soundproof_artist import SoundProofArtist
from src.domain.artist_status import ArtistStatus
from dataclasses import dataclass




@dataclass(frozen=True)
class ArtistMatch:
    """The SoundProof verdict for one artist name, with the database entry it was derived from."""

    artist_name: str
    status: ArtistStatus
    entry: SoundProofArtist | None
