from dataclasses import dataclass




@dataclass(frozen=True)
class TrackArtist:
    """An artist credited on a library track."""

    name: str
    # None when the artist is plain text without an artist page.
    channel_id: str | None
