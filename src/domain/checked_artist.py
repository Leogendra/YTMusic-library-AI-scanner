from src.domain.release_statistics import ReleaseStatistics
from collections.abc import Iterable
from dataclasses import dataclass




@dataclass(frozen=True)
class CheckedArtist:
    """An artist missing from SoundProof, with the statistics of its releases."""

    name: str
    channel_id: str
    statistics: ReleaseStatistics


def rank_checked_artists(checked_artists: Iterable[CheckedArtist]) -> list[CheckedArtist]:
    """Put first the artists whose releases are the most recent, which is typical of AI profiles publishing in bulk.

    Artists sharing the same mean year are ranked by their number of recent releases.
    """
    return sorted(
        checked_artists,
        key=lambda checked_artist: (checked_artist.statistics.mean_year, checked_artist.statistics.releases_last_2_years),
        reverse=True,
    )
