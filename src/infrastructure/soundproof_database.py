from src.domain.soundproof_artist import SoundProofArtist
from src.domain.artist_name import normalize_artist_name
from collections.abc import Iterable




class SoundProofDatabase:
    """In-memory index of the SoundProof artists, looked up by normalized artist name."""

    def __init__(self, artists: Iterable[SoundProofArtist]) -> None:
        self._artists_by_name: dict[str, SoundProofArtist] = {}
        for artist in artists:
            self._index(artist)

    def __len__(self) -> int:
        return len(self._artists_by_name)

    def find(self, artist_name: str) -> SoundProofArtist | None:
        return self._artists_by_name.get(normalize_artist_name(artist_name))

    def _index(self, artist: SoundProofArtist) -> None:
        # Two entries can collapse onto one normalized name: keep the one backed by the most votes.
        key = normalize_artist_name(artist.name)
        existing_artist = self._artists_by_name.get(key)
        if existing_artist is None or _total_votes(artist) > _total_votes(existing_artist):
            self._artists_by_name[key] = artist


def _total_votes(artist: SoundProofArtist) -> int:
    return artist.ai_votes + artist.human_votes
