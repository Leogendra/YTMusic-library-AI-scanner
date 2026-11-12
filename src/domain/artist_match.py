from src.domain.soundproof_artist import SoundProofArtist
from src.domain.artist_status import ArtistStatus
from src.domain.track_artist import TrackArtist
from dataclasses import dataclass




@dataclass(frozen=True)
class ArtistMatch:
    """The SoundProof verdict for one track artist, with the database entry it was derived from."""

    artist: TrackArtist
    status: ArtistStatus
    entry: SoundProofArtist | None
