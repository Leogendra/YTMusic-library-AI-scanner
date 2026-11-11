from pathlib import Path
import urllib.request
import json
import time

SOUNDPROOF_DUMP_URL = "https://raw.githubusercontent.com/NuclearBlox/SoundProof-Dumps/main/data/artists.json"

# The upstream dump is regenerated daily, so a fresher copy is pointless.
DEFAULT_MAX_AGE_SECONDS = 24 * 60 * 60

_DOWNLOAD_TIMEOUT_SECONDS = 60




class SoundProofDumpCache:
    """Local copy of the SoundProof artists dump, downloaded again once it is outdated."""

    def __init__(
        self,
        cache_file: Path,
        dump_url: str = SOUNDPROOF_DUMP_URL,
        max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS,
    ) -> None:
        self._cache_file = cache_file
        self._dump_url = dump_url
        self._max_age_seconds = max_age_seconds

    def load(self, force_refresh: bool = False) -> object:
        """Return the decoded JSON dump, downloading it first when the cache is missing, outdated or a refresh is forced."""
        if force_refresh or self._is_outdated():
            self._download()
        with self._cache_file.open(encoding="utf-8") as cache_stream:
            return json.load(cache_stream)

    def _is_outdated(self) -> bool:
        if not self._cache_file.exists():
            return True
        else:
            cache_age_seconds = time.time() - self._cache_file.stat().st_mtime
            return cache_age_seconds > self._max_age_seconds

    def _download(self) -> None:
        with urllib.request.urlopen(self._dump_url, timeout=_DOWNLOAD_TIMEOUT_SECONDS) as response:
            payload = response.read()
        # Decode before writing so a truncated or HTML error body never replaces a valid cache.
        json.loads(payload)
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)
        temporary_file = self._cache_file.with_suffix(".tmp")
        temporary_file.write_bytes(payload)
        temporary_file.replace(self._cache_file)
