from src.domain.classification import most_ai_voted_flagged_artist
from src.report.verdict_formatting import track_url
from src.domain.track_verdict import TrackVerdict
from pathlib import Path
import csv

class CsvReportFormatError(ValueError):
    """Raised when a CSV file does not have the columns of a report."""


CSV_COLUMNS: tuple[str, ...] = ("status", "is_verified", "ai_vote", "human_vote", "flagged_artist", "title", "url")




def build_csv_rows(verdicts: list[TrackVerdict], include_outvoted_artists: bool) -> list[dict[str, str]]:
    """Turn every verdict into one CSV row."""
    return [_build_row(verdict, include_outvoted_artists) for verdict in verdicts]


def read_csv_report(csv_file: Path) -> list[dict[str, str]]:
    with csv_file.open(encoding="utf-8-sig", newline="") as input_stream:
        reader = csv.DictReader(input_stream)
        if reader.fieldnames is not None and set(CSV_COLUMNS) <= set(reader.fieldnames):
            return list(reader)
        else:
            raise CsvReportFormatError(
                f"{csv_file} is not a report of this tool (expected columns: {', '.join(CSV_COLUMNS)}). Delete it and run again to generate it."
            )


def write_csv_report(verdicts: list[TrackVerdict], output_file: Path, include_outvoted_artists: bool) -> None:
    # utf-8-sig adds a BOM so that Excel detects the encoding of accented titles.
    with output_file.open("w", encoding="utf-8-sig", newline="") as output_stream:
        writer = csv.DictWriter(output_stream, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(build_csv_rows(verdicts, include_outvoted_artists))


def _build_row(verdict: TrackVerdict, include_outvoted_artists: bool) -> dict[str, str]:
    reference_artist = most_ai_voted_flagged_artist(verdict, include_outvoted_artists)
    ai_votes = reference_artist.ai_votes if reference_artist is not None else 0
    human_votes = reference_artist.human_votes if reference_artist is not None else 0
    is_verified = reference_artist is not None and reference_artist.verified
    return {
        "status": verdict.status.value,
        "is_verified": "yes" if is_verified else "no",
        "ai_vote": str(ai_votes),
        "human_vote": str(human_votes),
        "flagged_artist": reference_artist.name if reference_artist is not None else "",
        "title": verdict.track.title,
        "url": track_url(verdict) or "",
    }
