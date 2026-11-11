from src.domain.artist_status import ArtistStatus
from src.domain.track_verdict import TrackVerdict
from collections import Counter

_SUMMARY_LABELS: dict[ArtistStatus, str] = {
    ArtistStatus.AI: "AI",
    ArtistStatus.TIE: "Tied votes",
    ArtistStatus.HUMAN: "Human",
    ArtistStatus.UNKNOWN: "Not in SoundProof",
}




def render_console_report(verdicts: list[TrackVerdict]) -> str:
    """Render a summary of the analysis."""
    counts = Counter(verdict.status for verdict in verdicts)
    lines = [f"Analyzed {len(verdicts)} library tracks:"]
    lines.extend(f"  {label:<18} {counts[status]}" for status, label in _SUMMARY_LABELS.items())
    return "\n".join(lines)
