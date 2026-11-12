from src.application.artist_release_source import ArtistReleaseSource
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
import logging
import json
import time

# An AI profile can publish several releases a week, but the ranking only moves over months.
DEFAULT_MAX_AGE_SECONDS = 7 * 24 * 60 * 60

_LOGGER = logging.getLogger(__name__)




@dataclass(frozen=True)
class _CachedReleases:
    fetched_at: float
    release_years: list[int]


class ArtistReleaseCache:
    """Release source keeping on disk the release years of each artist, fetched again once outdated.

    Each artist expires on its own, so that a new artist of the library does not refresh the others. Failures are not cached and are retried on the next run.
    """

    def __init__(
        self,
        source: ArtistReleaseSource,
        cache_file: Path,
        force_refresh: bool = False,
        max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self._source = source
        self._cache_file = cache_file
        self._force_refresh = force_refresh
        self._max_age_seconds = max_age_seconds
        self._clock = clock
        self._entries = _read_entries(cache_file)

    def fetch_release_years(self, channel_id: str) -> list[int]:
        entry = self._entries.get(channel_id)
        if entry is not None and not self._force_refresh and not self._is_outdated(entry):
            return entry.release_years
        else:
            release_years = self._source.fetch_release_years(channel_id)
            self._entries[channel_id] = _CachedReleases(fetched_at=self._clock(), release_years=release_years)
            # Saved after each artist so that an interrupted run keeps what it already fetched.
            self._save()
            return release_years

    def _is_outdated(self, entry: _CachedReleases) -> bool:
        return self._clock() - entry.fetched_at > self._max_age_seconds

    def _save(self) -> None:
        payload = {
            channel_id: {"fetched_at": entry.fetched_at, "release_years": entry.release_years}
            for channel_id, entry in self._entries.items()
        }
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)
        temporary_file = self._cache_file.with_suffix(".tmp")
        temporary_file.write_text(json.dumps(payload), encoding="utf-8")
        temporary_file.replace(self._cache_file)


def _read_entries(cache_file: Path) -> dict[str, _CachedReleases]:
    if not cache_file.exists():
        return {}
    else:
        try:
            raw_entries = json.loads(cache_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            _LOGGER.warning("Ignored the unreadable release cache %s, it will be rebuilt.", cache_file)
            return {}
        return _parse_entries(raw_entries)


def _parse_entries(raw_entries: object) -> dict[str, _CachedReleases]:
    if not isinstance(raw_entries, dict):
        return {}
    else:
        entries: dict[str, _CachedReleases] = {}
        for channel_id, raw_entry in raw_entries.items():
            entry = _parse_entry(raw_entry)
            if entry is not None:
                entries[channel_id] = entry
        return entries


def _parse_entry(raw_entry: object) -> _CachedReleases | None:
    fetched_at = raw_entry.get("fetched_at") if isinstance(raw_entry, dict) else None
    release_years = raw_entry.get("release_years") if isinstance(raw_entry, dict) else None
    is_valid_date = isinstance(fetched_at, (int, float))
    is_valid_years = isinstance(release_years, list) and all(isinstance(year, int) for year in release_years)
    if is_valid_date and is_valid_years:
        return _CachedReleases(fetched_at=float(fetched_at), release_years=release_years)
    else:
        return None
