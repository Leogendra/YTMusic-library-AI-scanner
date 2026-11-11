from src.domain.classification import most_ai_voted_artist
from src.report.verdict_formatting import track_url
from src.domain.track_verdict import TrackVerdict
from pathlib import Path
import csv

CSV_COLUMNS: tuple[str, ...] = ("is_verified", "status", "ai_vote", "human_vote", "title", "artists", "album", "url")




def build_csv_rows(verdicts: list[TrackVerdict]) -> list[dict[str, str]]:
    """Turn every verdict into one CSV row."""
    return [_build_row(verdict) for verdict in verdicts]


def write_csv_report(verdicts: list[TrackVerdict], output_file: Path) -> None:
    # utf-8-sig adds a BOM so that Excel detects the encoding of accented titles.
    with output_file.open("w", encoding="utf-8-sig", newline="") as output_stream:
        writer = csv.DictWriter(output_stream, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(build_csv_rows(verdicts))


def _build_row(verdict: TrackVerdict) -> dict[str, str]:
    reference_artist = most_ai_voted_artist(verdict)
    ai_votes = reference_artist.ai_votes if reference_artist is not None else 0
    human_votes = reference_artist.human_votes if reference_artist is not None else 0
    is_verified = reference_artist is not None and reference_artist.verified
    return {
        "is_verified": "yes" if is_verified else "no",
        "status": verdict.status.value,
        "ai_vote": str(ai_votes),
        "human_vote": str(human_votes),
        "title": verdict.track.title,
        "artists": ", ".join(verdict.track.artist_names),
        "album": verdict.track.album_name or "",
        "url": track_url(verdict) or "",
    }
