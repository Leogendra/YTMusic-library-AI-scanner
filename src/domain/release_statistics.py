from collections.abc import Sequence
from dataclasses import dataclass
from statistics import fmean

# Only the release year is known, so "recent" covers the current year and the previous one.
RECENT_YEARS_SPAN = 2




@dataclass(frozen=True)
class ReleaseStatistics:
    """How recent and how many the releases (albums, EP and singles) of an artist are."""

    mean_year: float
    release_count: int
    releases_last_2_years: int
    first_year: int

    @property
    def recent_release_ratio(self) -> float:
        """Share of the releases published over the last two years, between 0 and 1."""
        return self.releases_last_2_years / self.release_count


def compute_release_statistics(release_years: Sequence[int], current_year: int) -> ReleaseStatistics | None:
    """Summarize the release years of an artist, or return None when the artist has no dated release."""
    if not release_years:
        return None
    else:
        first_recent_year = current_year - RECENT_YEARS_SPAN + 1
        return ReleaseStatistics(
            mean_year=fmean(release_years),
            release_count=len(release_years),
            releases_last_2_years=sum(1 for year in release_years if year >= first_recent_year),
            first_year=min(release_years),
        )
