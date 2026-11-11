from src.domain.artist_status import ArtistStatus
from src.domain.library_track import LibraryTrack
from src.domain.artist_match import ArtistMatch
from dataclasses import dataclass




@dataclass(frozen=True)
class TrackVerdict:
    """The verdict for a library track, aggregated from the verdicts of its artists."""

    track: LibraryTrack
    status: ArtistStatus
    artist_matches: tuple[ArtistMatch, ...]
