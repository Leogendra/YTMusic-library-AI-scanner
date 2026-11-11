from src.domain.classification import classify_artist, classify_track
from src.application.artist_database import ArtistDatabase
from src.application.library_source import LibrarySource
from src.domain.library_track import LibraryTrack
from src.domain.track_verdict import TrackVerdict
from src.domain.artist_match import ArtistMatch




def analyze_library(source: LibrarySource, database: ArtistDatabase) -> list[TrackVerdict]:
    """Classify every track of the library against the artist database."""
    return [analyze_track(track, database) for track in source.fetch_tracks()]


def analyze_track(track: LibraryTrack, database: ArtistDatabase) -> TrackVerdict:
    """Classify one track from the verdicts of all its artists."""
    artist_matches = tuple(_match_artist(artist_name, database) for artist_name in track.artist_names)
    status = classify_track(match.status for match in artist_matches)
    return TrackVerdict(track=track, status=status, artist_matches=artist_matches)


def _match_artist(artist_name: str, database: ArtistDatabase) -> ArtistMatch:
    entry = database.find(artist_name)
    return ArtistMatch(artist_name=artist_name, status=classify_artist(entry), entry=entry)
