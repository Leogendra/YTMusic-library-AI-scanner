from dataclasses import dataclass




@dataclass(frozen=True)
class LibraryTrack:
    """A song saved in the user's music library."""

    video_id: str | None
    title: str
    artist_names: tuple[str, ...]
    album_name: str | None
