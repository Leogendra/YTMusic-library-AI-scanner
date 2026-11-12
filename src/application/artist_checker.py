from src.application.artist_release_source import ArtistReleaseSource, ArtistReleasesUnavailableError
from src.domain.release_statistics import ReleaseStatistics, compute_release_statistics
from src.domain.checked_artist import CheckedArtist, rank_checked_artists
from src.domain.artist_check_report import ArtistCheckReport
from src.domain.track_artist import TrackArtist
from collections.abc import Callable, Sequence
import logging

_LOGGER = logging.getLogger(__name__)

# Called after each artist with the number of artists already checked and the total number of artists.
ProgressCallback = Callable[[int, int], None]




def check_artists(
    artists: Sequence[TrackArtist],
    source: ArtistReleaseSource,
    current_year: int,
    on_progress: ProgressCallback,
) -> ArtistCheckReport:
    """Rank the artists by the recency of their releases, leaving aside the artists that cannot be verified."""
    checked_artists: list[CheckedArtist] = []
    for checked_count, artist in enumerate(artists, start=1):
        statistics = _fetch_statistics(artist, source, current_year)
        if statistics is not None and artist.channel_id is not None:
            checked_artists.append(CheckedArtist(name=artist.name, channel_id=artist.channel_id, statistics=statistics))
        on_progress(checked_count, len(artists))
    return ArtistCheckReport(
        checked_artists=tuple(rank_checked_artists(checked_artists)),
        unverifiable_artist_count=len(artists) - len(checked_artists),
    )


def _fetch_statistics(artist: TrackArtist, source: ArtistReleaseSource, current_year: int) -> ReleaseStatistics | None:
    if artist.channel_id is None:
        return None
    else:
        try:
            release_years = source.fetch_release_years(artist.channel_id)
        except ArtistReleasesUnavailableError as error:
            _LOGGER.info("Skipped the artist %s: %s", artist.name, error)
            return None
        else:
            return compute_release_statistics(release_years, current_year)
