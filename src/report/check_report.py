from src.domain.checked_artist import CheckedArtist
from collections.abc import Iterable
from pathlib import Path
import csv

YOUTUBE_MUSIC_CHANNEL_URL = "https://music.youtube.com/channel/"

CHECK_CSV_COLUMNS: tuple[str, ...] = ("artist", "mean_year", "release_count", "releases_last_2_years", "first_year", "url")




def write_check_report(checked_artists: Iterable[CheckedArtist], output_file: Path) -> None:
    # utf-8-sig adds a BOM so that Excel detects the encoding of accented names.
    with output_file.open("w", encoding="utf-8-sig", newline="") as output_stream:
        writer = csv.DictWriter(output_stream, fieldnames=CHECK_CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(_build_row(checked_artist) for checked_artist in checked_artists)


def _build_row(checked_artist: CheckedArtist) -> dict[str, str]:
    statistics = checked_artist.statistics
    return {
        "artist": checked_artist.name,
        "mean_year": f"{statistics.mean_year:.2f}",
        "release_count": str(statistics.release_count),
        "releases_last_2_years": str(statistics.releases_last_2_years),
        "first_year": str(statistics.first_year),
        "url": YOUTUBE_MUSIC_CHANNEL_URL + checked_artist.channel_id,
    }
