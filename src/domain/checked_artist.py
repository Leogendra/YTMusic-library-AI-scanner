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
    """Put first the artists who started publishing the most recently, which is typical of AI profiles publishing in bulk.

    Artists sharing the same year of first release are ranked by their number of releases over the last two years.
    """
    return sorted(
        checked_artists,
        key=lambda checked_artist: (checked_artist.statistics.first_year, checked_artist.statistics.releases_last_2_years),
        reverse=True,
    )
