from src.application.artist_release_source import ArtistReleasesUnavailableError
from ytmusicapi.exceptions import YTMusicError
from typing import Any, Protocol
import json

# EP are listed in the albums section, so these two sections cover every release.
_RELEASE_SECTIONS: tuple[str, ...] = ("albums", "singles")




class ArtistClient(Protocol):
    """The subset of the ytmusicapi client this adapter relies on."""

    def get_artist(self, channelId: str) -> dict[str, Any]: ...

    def get_artist_albums(self, channelId: str, params: str, limit: int | None = 100) -> list[dict[str, Any]]: ...


class YTMusicArtistReleases:
    """Release source reading the artist pages of YouTube Music."""

    def __init__(self, client: ArtistClient) -> None:
        self._client = client

    def fetch_release_years(self, channel_id: str) -> list[int]:
        try:
            raw_artist = self._client.get_artist(channel_id)
            return [year for section_name in _RELEASE_SECTIONS for year in self._fetch_section_years(raw_artist.get(section_name))]
        # ytmusicapi raises KeyError, IndexError or TypeError when the page does not have the layout of an artist page.
        except (YTMusicError, json.JSONDecodeError, KeyError, IndexError, TypeError) as error:
            raise ArtistReleasesUnavailableError(f"Cannot read the releases of the channel {channel_id}: {error}") from error

    def _fetch_section_years(self, raw_section: object) -> list[int]:
        if not isinstance(raw_section, dict):
            return []
        else:
            return [year for year in map(_parse_year, self._fetch_section_releases(raw_section)) if year is not None]

    def _fetch_section_releases(self, raw_section: dict[str, Any]) -> list[dict[str, Any]]:
        browse_id = raw_section.get("browseId")
        params = raw_section.get("params")
        # Without params, the section has no "See all" page and its results already hold every release.
        if isinstance(browse_id, str) and isinstance(params, str):
            return self._client.get_artist_albums(browse_id, params, limit=None)
        else:
            return raw_section.get("results") or []


def _parse_year(raw_release: object) -> int | None:
    year = raw_release.get("year") if isinstance(raw_release, dict) else None
    if isinstance(year, str) and year.isdigit():
        return int(year)
    else:
        return None
