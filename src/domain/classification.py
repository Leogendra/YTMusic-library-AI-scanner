from src.domain.soundproof_artist import SoundProofArtist
from src.domain.artist_status import ArtistStatus
from src.domain.track_verdict import TrackVerdict
from collections.abc import Iterable

MINIMUM_AI_VOTES = 1

# When a track has several artists, the most alarming verdict wins: one AI artist is enough to flag the track.
_STATUS_PRIORITY: tuple[ArtistStatus, ...] = (
    ArtistStatus.AI,
    ArtistStatus.TIE,
    ArtistStatus.HUMAN,
    ArtistStatus.UNKNOWN,
)




def classify_artist(entry: SoundProofArtist | None) -> ArtistStatus:
    """Classify an artist from its SoundProof votes.

    The precomputed "votes" field of the dump is ignored because it does not always equal ai_votes - human_votes.
    """
    if entry is None:
        return ArtistStatus.UNKNOWN
    elif entry.ai_votes > entry.human_votes:
        return ArtistStatus.AI
    elif entry.ai_votes < entry.human_votes:
        return ArtistStatus.HUMAN
    else:
        return ArtistStatus.TIE


def classify_track(artist_statuses: Iterable[ArtistStatus]) -> ArtistStatus:
    """Aggregate the verdicts of a track's artists into the verdict of the track."""
    present_statuses = set(artist_statuses)
    for status in _STATUS_PRIORITY:
        if status in present_statuses:
            return status
    return ArtistStatus.UNKNOWN


def has_ai_votes(entry: SoundProofArtist | None) -> bool:
    """Tell whether the community reported the artist as AI at least once, even if human votes outnumber them."""
    return entry is not None and entry.ai_votes >= MINIMUM_AI_VOTES


def select_tracks_with_ai_votes(verdicts: Iterable[TrackVerdict]) -> list[TrackVerdict]:
    """Keep the tracks having at least one artist with an AI vote, whatever the overall verdict."""
    return [
        verdict
        for verdict in verdicts
        if any(has_ai_votes(match.entry) for match in verdict.artist_matches)
    ]


def most_ai_voted_artist(verdict: TrackVerdict) -> SoundProofArtist | None:
    """Return the artist of the track with the most AI votes, or None when no artist has any.

    It is the single reference for the AI votes and the verification flag shown for a track, so both always describe the same artist.
    """
    ai_voted_entries = [
        match.entry for match in verdict.artist_matches if match.entry is not None and has_ai_votes(match.entry)
    ]
    return max(ai_voted_entries, key=lambda entry: entry.ai_votes, default=None)
