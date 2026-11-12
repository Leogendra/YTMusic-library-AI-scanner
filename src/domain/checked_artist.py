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
    """Put first the artists whose releases are mostly recent, which is typical of AI profiles publishing in bulk.

    Artists sharing the same share of recent releases are ranked by their number of recent releases, then by the year of
    their first release, the latest first.
    """
    return sorted(
        checked_artists,
        key=lambda checked_artist: (
            checked_artist.statistics.recent_release_ratio,
            checked_artist.statistics.releases_last_2_years,
            checked_artist.statistics.first_year,
        ),
        reverse=True,
    )
