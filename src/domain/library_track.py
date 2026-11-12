from src.domain.track_artist import TrackArtist
from dataclasses import dataclass




@dataclass(frozen=True)
class LibraryTrack:
    """A song saved in the user's music library."""

    video_id: str | None
    title: str
    artists: tuple[TrackArtist, ...]
    album_name: str | None
