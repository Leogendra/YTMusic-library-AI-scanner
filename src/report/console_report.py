from src.report.verdict_formatting import describe_artist_match, decisive_artist_matches
from src.domain.artist_status import ArtistStatus
from src.domain.track_verdict import TrackVerdict
from collections import Counter

_SECTION_TITLES: dict[ArtistStatus, str] = {
    ArtistStatus.AI: "Tracks by AI artists",
    ArtistStatus.TIE: "Tracks with tied votes (undecided)",
}

_SUMMARY_LABELS: dict[ArtistStatus, str] = {
    ArtistStatus.AI: "AI",
    ArtistStatus.TIE: "Tied votes",
    ArtistStatus.HUMAN: "Human",
    ArtistStatus.UNKNOWN: "Not in SoundProof",
}




def render_console_report(verdicts: list[TrackVerdict]) -> str:
    """Render a summary of the analysis followed by the list of flagged tracks."""
    lines = _render_summary(verdicts)
    for status, title in _SECTION_TITLES.items():
        lines.extend(_render_section(title, [verdict for verdict in verdicts if verdict.status is status]))
    return "\n".join(lines)


def _render_summary(verdicts: list[TrackVerdict]) -> list[str]:
    counts = Counter(verdict.status for verdict in verdicts)
    lines = [f"Analyzed {len(verdicts)} library tracks:"]
    lines.extend(f"  {label:<18} {counts[status]}" for status, label in _SUMMARY_LABELS.items())
    return lines


def _render_section(title: str, verdicts: list[TrackVerdict]) -> list[str]:
    if not verdicts:
        return []
    else:
        lines = ["", f"{title} ({len(verdicts)}):"]
        for verdict in sorted(verdicts, key=lambda verdict: verdict.track.title.casefold()):
            artists = ", ".join(describe_artist_match(match) for match in decisive_artist_matches(verdict))
            lines.append(f"  - {verdict.track.title} by {artists}")
        return lines
